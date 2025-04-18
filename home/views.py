from django.shortcuts import render, get_object_or_404
from animais.models import Animais, tipoAnimal
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    types = tipoAnimal.objects.all()
    tipo_id = request.GET.get('tipo_id')
    data_types = []

    for type in types:
        total = Animais.objects.filter(tipo_animal=type, disponivel_para_adocao=True).count()
        
        data_types.append({
            'type': type,
            'total': total
        })

    # Verifica se o tipo_id existe
    if tipo_id:
        try:
            tipo_selecionado = tipoAnimal.objects.get(id=tipo_id)
        except tipoAnimal.DoesNotExist:
            tipo_selecionado = types[0]
    else:
        tipo_selecionado = types[0]

    # Filtra os animais disponíveis para adoção
    animais = Animais.objects.filter(tipo_animal=tipo_selecionado, disponivel_para_adocao=True)

    # Paginação dos resultados
    paginator = Paginator(animais, 8)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)

    # Contexto para o template
    context = {
        'first_type': tipo_selecionado,
        'data_types': data_types,
        'animals': page_obj
    }

    return render(request, 'home/index.html', context)  

def animal_detail(request, id):
    animal = get_object_or_404(Animais, id=id)
    return render(request, 'home/animal.html', {'animal': animal})
