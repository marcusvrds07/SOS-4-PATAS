from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import TipoAnimal
import json
from django.utils.timezone import now
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Animais, AnimaisAdotados



# Create your views here.

@csrf_exempt
def delete_tipoanimal_ajax(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        pk = data.get("id")
        try:
            obj = TipoAnimal.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({"success": True})
        except TipoAnimal.DoesNotExist:
            return JsonResponse({"success": False, "error": "Categoria não encontrada"})
    return JsonResponse({"success": False, "error": "Método inválido"})

@csrf_exempt
def edit_tipoanimal_ajax(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        pk = data.get("id")
        nome = data.get("nome")
        try:
            obj = TipoAnimal.objects.get(pk=pk)
            obj.nome = nome
            obj.save()
            return JsonResponse({"success": True})
        except TipoAnimal.DoesNotExist:
            return JsonResponse({"success": False, "error": "Categoria não encontrada"})
    return JsonResponse({"success": False, "error": "Método inválido"})


@csrf_exempt
def add_tipoanimal_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        nome = data.get("nome")
        if not nome:
            return JsonResponse({"success": False, "error": "Nome não informado"}, status=400)
        if TipoAnimal.objects.filter(nome=nome).exists():
            return JsonResponse({"success": False, "error": "Já existe"}, status=400)
        obj = TipoAnimal.objects.create(nome=nome)
        return JsonResponse({"success": True, "id": obj.id, "nome": obj.nome})
    return JsonResponse({"success": False, "error": "Método inválido"}, status=405)

@require_POST
def marcar_adotado(request, animal_id):
    animal = get_object_or_404(Animais, id=animal_id)

    # Pegando dados do formulário do adotante
    nome_adotante = request.POST.get("nome_adotante")
    telefone_adotante = request.POST.get("telefone_adotante")
    email_adotante = request.POST.get("email_adotante")
    endereco_adotante = request.POST.get("endereco_adotante")

    if not all([nome_adotante, telefone_adotante, email_adotante, endereco_adotante]):
        messages.error(request, "Por favor, preencha todos os campos do adotante.")
        return redirect(request.META.get('HTTP_REFERER', '/admin/animais/animais/'))

    # Criar registro em AnimaisAdotados
    adotado = AnimaisAdotados.objects.create(
        nome=animal.nome,
        especie=animal.especie,
        idade_anos=animal.idade_anos,
        nome_adotante=nome_adotante,
        telefone_adotante=telefone_adotante,
        email_adotante=email_adotante,
        endereco_adotante=endereco_adotante,
        # copie outros campos se houver...
    )

    # Remover animal da tabela de disponíveis
    animal.delete()

    messages.success(request, f"O animal {adotado.nome} foi adotado com sucesso!")

    # Redireciona para a lista de animais no admin
    return redirect('/admin/animais/animais/')