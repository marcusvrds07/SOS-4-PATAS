from django.shortcuts import render
from animais.models import Animais
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    animais = Animais.objects.all()
    paginator = Paginator(animais, 8)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    context = {
        'animals': page_obj
    }
    return render(request, 'home/index.html', context)

def animal(request, id):
    animals = Animais.objects.all()
    animal_found = {}

    for animal in animals:
        if animal.id == id:
            animal_found = animal
            break

    return render(request, 'home/animal.html', {'animal': animal_found})
