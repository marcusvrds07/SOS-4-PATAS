from django.shortcuts import render, get_object_or_404
from animais.models import Animais, TipoAnimal
from django.core.paginator import Paginator
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
import re

# Create your views here.

def home(request):
    types = TipoAnimal.objects.all()
    type_id = request.GET.get('tipo_id')
    data_types = []
    context = {}

    for type in types:
        total = Animais.objects.filter(especie=type, disponivel_para_adocao=True).count()
        
        data_types.append({
            'type': type,
            'total': total
        })

    # Verifica se o tipo_id existe
    if types:
        if type_id:
            try:
                type_selected = TipoAnimal.objects.get(id=type_id)
            except TipoAnimal.DoesNotExist:
                type_selected = types[0]
        else:
            type_selected = types[0]
    else:
        type_selected = None
    
    if type_selected:
        # Filtra os animais disponíveis para adoção
        animais = Animais.objects.filter(especie=type_selected, disponivel_para_adocao=True)

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
            elif days.months > 0:
                if days.months > 1:
                        month = 'meses'
                animal.data_nascimento = f'{days.months} {month}'
            else:
                animal.data_nascimento = 'Não informado'

        # Contexto para o template
        context = {
            'title': 'Inicio',
            'first_type': type_selected,
            'data_types': data_types,
            'animals': page_obj,
            'has_types': True,
        }
    else:
        context = {
        'title': 'Inicio',
        'first_type': 'Nenhum Campo',
        'data_types': [],
        'animals': [],
        'has_types': False,
        'empty_message': 'Nenhum tipo de animal foi cadastrado ainda.',
    }

    return render(request, 'home/index.html', context)  

def animal_detail(request, id):
    animal = get_object_or_404(Animais, id=id)

    days = relativedelta(date.today(), animal.data_nascimento)
    year = 'ano'
    month = 'mês'

    if days.years > 0:
        if days.years > 1:
            year = 'anos'
        if days.months > 0:
            if days.months > 1:
                month = 'meses'
            animal.data_nascimento = f'{days.years} {year} e {days.months} {month}'
        else:
            if days.years > 1:
                    year = 'anos'
            animal.data_nascimento = f'{days.years} {year}'
    elif days.months > 0:
        if days.months > 1:
                month = 'meses'
        animal.data_nascimento = f'{days.months} {month}'
    else:
        animal.data_nascimento = 'Não informado'

    return render(request, 'home/animalpag.html', {'animal': animal})

def voluntario_sucesso(request):
    return render(request, "home/voluntario_sucesso.html")

def voluntario(request):

    context = {
        'title': 'Voluntário',
    }

    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        mensagem = request.POST.get("mensagem")
        telefone_limpo = re.sub(r'\D', '', telefone)

        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string

        assunto = f"Nova inscrição de voluntário: {nome}"
        html_content = render_to_string("emails/voluntario_email.html", {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "mensagem": mensagem,
            "telefone_limpo": telefone_limpo,
        })

        email_msg = EmailMultiAlternatives(
            assunto,
            "",  
            to=["ong.sos4patas0@gmail.com"]
        )
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()

        messages.success(request, "Inscrição enviada com sucesso! Entraremos em contato em breve.")

        return redirect("home:voluntarios")
    return render(request, "home/voluntarios.html", context)