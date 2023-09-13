import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
import graphql_jwt
from graphql_jwt.shortcuts import get_token

from django.contrib.auth import get_user_model,authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import random

from .models import User, CarOwner


# Define GraphQL types
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class CarOwnerType(DjangoObjectType):
    class Meta:
        model = CarOwner

# Define input types
class UserInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    is_car_owner = graphene.Boolean()
    is_superuser= graphene.Boolean(required=True)
    is_staff= graphene.Boolean(required=True)

class CreateUserInput(UserInput):
    password = graphene.String(required=True)
    confirm_password = graphene.String(required=True)

class ForgotPasswordInput(graphene.InputObjectType):
    email = graphene.String(required=True)

class ResendOtpInput(graphene.InputObjectType):
    email = graphene.String(required=True)

class ResetPasswordInput(graphene.InputObjectType):
    otp = graphene.Int(required=True)
    new_password = graphene.String(required=True)
    confirm_password = graphene.String(required=True)

class VerifyAccountInput(graphene.InputObjectType):
    otp = graphene.Int(required=True)
    email = graphene.String(required=True)

class UserLoginInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)

# Define mutations
class  CreateSuperUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        input = CreateUserInput(required=True)

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, input):

        password = input.get('password')
        confirm_password = input.get('confirm_password')

        if password != confirm_password:
            raise GraphQLError("Passwords do not match.")

        if input.is_superuser==True and input.is_staff==True and not input.is_car_owner:
            user = get_user_model()(
                email=input.email,
                first_name=input.first_name,
                last_name=input.last_name,
                is_superuser=input.is_superuser,
                is_staff=input.is_staff
            )

            user.set_password(password)
            user.save()

            return CreateSuperUser(user=user)
        
class CreateUser(graphene.Mutation):
    user = graphene.Field(CarOwnerType)

    class Arguments:
        input = CreateUserInput(required=True)

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, input):

        password = input.get('password')
        confirm_password = input.get('confirm_password')

        if password != confirm_password:
            raise GraphQLError("Passwords do not match.")

        if not input.is_superuser and not input.is_staff and input.is_car_owner==True:

            otp = random.randint(1000, 9999)

            subject = "Activate Your Account"
            message = f"Your OTP (One-Time Password) is: {otp}"
            email_from = settings.EMAIL_HOST
            recipient_list = [input.email]

            send_mail(subject, message, email_from, recipient_list)

            otp_expiration = timezone.now() + timedelta(minutes=5)

            user = get_user_model()(
                email=input.email,
                first_name=input.first_name,
                last_name=input.last_name,
                is_car_owner=input.is_car_owner,
                otp=otp,
                otp_expiration=otp_expiration,
            )

            user.set_password(password)
            user.save()

            return CreateUser(user=user)

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, id, input):
        try:
            user = get_user_model().objects.get(id=id)
        except get_user_model().DoesNotExist:
            raise GraphQLError(f"User with id {id} does not exist.")

        # Update user attributes based on input fields
        for field, value in input.items():
            setattr(user, field, value)

        # Check if password and confirm_password match
        password = input.get("password")
        confirm_password = input.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise GraphQLError("Passwords do not match.")

        # If a new password is provided, set it
        if password:
            user.set_password(password)

        user.save()

        return UpdateUser(user=user)

class DeleteUser(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, id):
        user = User.objects.get(pk=id)
        user.delete()
        return DeleteUser(success=True)

class ForgotPassword(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        input = ForgotPasswordInput()

    @classmethod
    def mutate(cls, root, info, input):
        email = input.get('email')

        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise GraphQLError("User with this email address does not exist.")

        otp = random.randint(1000, 9999)        

        subject = "Password Reset OTP"
        message = f"Your OTP (One-Time Password) is: {otp}"
        email_from = settings.EMAIL_HOST
        recipient_list = [user.email]  # Fix the recipient list

        send_mail(subject, message, email_from, recipient_list)

        otp_expiration = timezone.now() + timedelta(minutes=5)

        user.otp = otp
        user.otp_expiration = otp_expiration
        user.save()

        return ForgotPassword(success=True)

class ResetPassword(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        input = ResetPasswordInput()

    @classmethod
    def mutate(cls, root, info, input):
        otp = input.get('otp')
        new_password = input.get('new_password')
        confirm_password = input.get('confirm_password')

        if new_password != confirm_password:
            raise GraphQLError("Passwords do not match.")

        User = get_user_model()

        try:
            user = User.objects.get(otp=otp)
        except User.DoesNotExist:
            raise GraphQLError("User with this OTP does not exist.")

        if user.otp != otp or not user.is_otp_valid():
            raise GraphQLError("Invalid OTP or OTP has expired.")

        user.set_password(new_password)
        user.clear_otp()
        user.save()

        return ResetPassword(success=True)

class VerifyAccount(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        input=VerifyAccountInput()

    @classmethod
    def mutate(cls, root, info, input):
        User = get_user_model()

        otp = input.get('otp')
        email = input.get('email')        

        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            raise GraphQLError("User with this Email does not exist.")

        print(f"Is OTP valid: {user.is_otp_valid()}")
        
        if user.is_otp_match(otp):

            user.is_verified = True
            user.clear_otp()
            user.save()

            return VerifyAccount(success=True, message="OTP verification successful.")
        else:
            return VerifyAccount(success=False, message="OTP verification failed.")

class ResendOtp(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        input = ResendOtpInput()

    @classmethod
    def mutate(cls, root, info, input):
        email = input.get('email')

        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise GraphQLError("User with this email address does not exist.")

        otp = random.randint(1000, 9999)        

        subject = "Password Reset OTP"
        message = f"Your OTP (One-Time Password) is: {otp}"
        email_from = settings.EMAIL_HOST
        recipient_list = [user.email]

        send_mail(subject, message, email_from, recipient_list)

        otp_expiration = timezone.now() + timedelta(minutes=5)

        user.otp = otp
        user.otp_expiration = otp_expiration
        user.save()

        return ResendOtp(success=True)

class UserLogin(graphene.Mutation):
     
    class Arguments:
        input = UserLoginInput(required=True)

    success = graphene.Boolean()
    token = graphene.String()
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, input):
        email = input.email
        password = input.password

        if not email or not password:
            raise GraphQLError("Must include both email and password.")

        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise GraphQLError("User with this email address does not exist.")
        
        if not user.is_verified:
            raise GraphQLError("You must verify your account!")

        authenticated_user = authenticate(request=info.context, email=email, password=password)

        if authenticated_user:
            token = get_token(authenticated_user)

            return cls(success=True, token=token, user=authenticated_user)
        else:
            raise GraphQLError("Unable to log in with provided credentials.")

# Define the GraphQL schema
class AuthQuery(graphene.ObjectType):
    users = graphene.List(UserType)
    car_owners = graphene.List(CarOwnerType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_car_wash_owners(self, info):
        return CarWashOwner.objects.all()

    def resolve_car_owners(self, info):
        return CarOwner.objects.all()

class AuthMutations(graphene.ObjectType):
    create_superuser= CreateSuperUser.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    forgot_password = ForgotPassword.Field()
    reset_password = ResetPassword.Field()
    verify_account = VerifyAccount.Field()
    resend_otp=ResendOtp.Field()
    login = UserLogin.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

# schema = graphene.Schema(query=Query, mutation=Mutation)

