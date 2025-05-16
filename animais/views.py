from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import TipoAnimal
import json

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
