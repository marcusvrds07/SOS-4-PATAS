from django.shortcuts import render
from animais.models import Animais
from django.contrib.auth.models import User
from django.contrib.admin.sites import site
from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import json

@csrf_exempt
def change_password_ajax(request, user_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Não autenticado.'})

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Requisição inválida.'})

    if not (request.user.is_superuser or request.user.pk == int(user_id)):
        return JsonResponse({'success': False, 'error': 'Sem permissão.'})

    try:
        data = json.loads(request.body)
        new_password = data.get('password', '')
    except Exception:
        return JsonResponse({'success': False, 'error': 'Dados inválidos.'})

    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuário não encontrado.'})

    try:
        validate_password(new_password, user=user)
    except Exception as e:
        error_msgs = [str(msg) for msg in e.error_list] if hasattr(e, 'error_list') else [str(e)]
        return JsonResponse({'success': False, 'error': ' '.join(error_msgs)})

    user.set_password(new_password)
    user.save()
    return JsonResponse({'success': True})


@login_required
def dashboard_admin(request):
    animais = Animais.objects.filter(disponivel_para_adocao=True).count()
    voluntarios = User.objects.filter(is_active=True).count()
    adocoes = 0

    ultimas_acoes = LogEntry.objects.select_related('content_type', 'user') \
        .filter(user=request.user).order_by('-action_time')[:5]

    return render(request, 'admin/index.html', {
        'app_list': site.get_app_list(request),
        'animais_disponiveis': animais,
        'voluntarios_ativos': voluntarios,
        'adocoes_concluidas': adocoes,
        'admin_log': ultimas_acoes,
    })

