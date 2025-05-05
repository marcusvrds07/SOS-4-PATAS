from django.shortcuts import render
from animais.models import Animais
from django.contrib.auth.models import User
from django.contrib.admin.sites import site

def dashboard_admin(request):
    animais = Animais.objects.filter(disponivel_para_adocao=True).count()
    voluntarios = User.objects.filter(is_active=True).count()
    adocoes = 0

    return render(request, 'admin/index.html', {
        'app_list': site.get_app_list(request),
        'animais_disponiveis': animais,
        'voluntarios_ativos': voluntarios,
        'adocoes_concluidas': adocoes
    })

