from django.shortcuts import render, get_object_or_404
from animais.models import Animais, tipoAnimal
from django.core.paginator import Paginator
from datetime import date
from dateutil.relativedelta import relativedelta

# Create your views here.

def home(request):
    types = tipoAnimal.objects.all()
    type_id = request.GET.get('tipo_id')
    data_types = []
    context = {}

    for type in types:
        total = Animais.objects.filter(tipo_animal=type, disponivel_para_adocao=True).count()
        
        data_types.append({
            'type': type,
            'total': total
        })

    # Verifica se o tipo_id existe
    if types:
        if type_id:
            try:
                type_selected = tipoAnimal.objects.get(id=type_id)
            except tipoAnimal.DoesNotExist:
                type_selected = types[0]
        else:
            type_selected = types[0]
    else:
        type_selected = None
    
    if type_selected:
        # Filtra os animais disponíveis para adoção
        animais = Animais.objects.filter(tipo_animal=type_selected, disponivel_para_adocao=True)

        # Paginação dos resultados
        paginator = Paginator(animais, 10)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        for animal in page_obj:
            days = relativedelta(date.today(), animal.data_nascimento)
            year = 'ano'
            month = 'mês'

            if days.years > 0:
                if days.years > 1:
                    year = 'anos'
                animal.data_nascimento = f'{days.years} {year}'
            else:
                if days.months > 1:
                        month = 'meses'
                animal.data_nascimento = f'{days.months} {month}'




        # Contexto para o template
        context = {
            'first_type': type_selected,
            'data_types': data_types,
            'animals': page_obj,
            'has_types': True,
        }
    else:
        context = {
        'first_type': 'Nenhum Campo',
        'data_types': [],
        'animals': [],
        'has_types': False,
        'empty_message': 'Nenhum tipo de animal foi cadastrado ainda.',
    }

    return render(request, 'home/index.html', context)  

def animal_detail(request, id):
    animal = get_object_or_404(Animais, id=id)
    return render(request, 'home/animalpag.html', {'animal': animal})