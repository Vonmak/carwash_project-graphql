# myapp/choices.py

from carly.models import CarMake, CarModel

def get_car_make_choices():
    return [(make.name, make.name) for make in CarMake.objects.all()]

def get_car_model_choices():
    return [(model.name, model.name) for model in CarModel.objects.all()]
