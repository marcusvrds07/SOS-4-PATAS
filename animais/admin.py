from django.contrib import admin
from animais import models

# Register your models here.

@admin.register(models.Animais)
class AnimalAdmin(admin.ModelAdmin):
    list_display = 'id', 'nome', 'idade', 'foto',
    ordering = ['-id']