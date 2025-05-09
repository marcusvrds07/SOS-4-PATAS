from django.contrib import admin
from animais import models
from django.utils.html import format_html
from django.urls import reverse
from django.templatetags.static import static
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
    list_display = 'id', 'nome', 'data_nascimento', 'preview', 'acoes', 
    readonly_fields = ['data_nascimento']
    search_fields = ['nome', 'id', 'data_nascimento']
    list_filter = ['tipo_animal']
    list_per_page = 5
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

    def acoes(self, obj):
        change_url = reverse('admin:animais_animais_change', args=[obj.pk])
        delete_url = reverse('admin:animais_animais_delete', args=[obj.pk])
        edit_icon   = static('global/imgs/lapis.png')
        delete_icon = static('global/imgs/x.png')
        return format_html(
            '<a href="{}"><img class="action-icon" src="{}" alt="Editar" title="Editar"/></a> '
            '<a href="{}"><img class="action-icon" src="{}" alt="Excluir" title="Excluir"/></a>',
            change_url, edit_icon, delete_url, delete_icon
        )
    acoes.short_description = 'Ações'