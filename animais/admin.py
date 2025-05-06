from django.contrib import admin
from animais import models
from django.utils.html import format_html
from .forms import AnimalForm

# Register your models here.

class AnimalImageInline(admin.TabularInline):
    model = models.AnimalImage
    extra = 1
    readonly_fields = ['preview']
    fields = ['image','preview']

    def preview(self, obj):
        if obj.image:
            try:
                return format_html(f'<img src="{obj.image.url}" width="80" style="object-fit:contain;" />')
            except ValueError:
                return "Imagem não encontrada"
        return "-"

@admin.register(models.tipoAnimal)
class tipoAnimal(admin.ModelAdmin):
    list_display = 'tipo_animal',

@admin.register(models.Animais)
class AnimalAdmin(admin.ModelAdmin):
    inlines = [AnimalImageInline]
    list_display = 'id', 'nome', 'anos', 'meses', 'preview',
    ordering = ['-id']
    form = AnimalForm

    def preview(self, obj):
        if obj.foto:
            try:
                return format_html(f'<img src="{obj.foto.url}" width="55" style="object-fit:contain;" />')
            except ValueError:
                return "Imagem não encontrada"
        return "-"
    preview.short_description = 'Foto da Capa'