from django.shortcuts import render
from animais.models import Animais

# Create your views here.

def home(request):
    animais = Animais.objects.all()
    context = {
        'animais': animais
    }
    return render(request, 'home/index.html', context)