from django.contrib import admin
from animais import models

# Register your models here.

class AnimalImageInline(admin.TabularInline):
    model = models.AnimalImage
    extra = 1

@admin.register(models.Animais)
class AnimalAdmin(admin.ModelAdmin):
    inlines = [AnimalImageInline]
    list_display = 'id', 'nome', 'idade', 'foto',
    ordering = ['-id']