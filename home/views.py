from django.shortcuts import render
from animais.models import Animais

# Create your views here.

def home(request):
    animais = Animais.objects.all()
    context = {
        'animais': animais
    }
    return render(request, 'home/index.html', context)

def animal(request, id):
    animals = Animais.objects.all()
    animal_found = {}

    for animal in animals:
        if animal.id == id:
            animal_found = animal

    return render(request, 'home/animal.html', {'animal': animal_found})
