from django.shortcuts import render, get_object_or_404
from animais.models import Animais, tipoAnimal
from django.core.paginator import Paginator

# Create your views here.

#teste

def home(request):
    types = tipoAnimal.objects.all()
    data_types = []
    for type in types:
        total = Animais.objects.filter(tipo_animal=type).count()
        
        data_types.append({
            'type': type,
            'total': total
        })

    context = {
        'data_types': data_types
    }
    return render(request, 'home/index.html', context)

def animal_by_type(request, tipo_id):
    # Obtém o tipo de animal selecionado
    type = get_object_or_404(tipoAnimal, id=tipo_id)
    
    animals = Animais.objects.filter(tipo_animal=type, disponivel_para_adocao=True)
    
    # Paginação dos animais
    paginator = Paginator(animals, 8)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    
    context = {
        'type': type,
        'animals': page_obj
    }
    return render(request, 'home/animal_by_type.html', context)

def animal_details(request, id):
    animal_found = get_object_or_404(Animais, pk=id)
    return render(request, 'home/animal.html', {'animal': animal_found})
