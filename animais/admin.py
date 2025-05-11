from django.contrib import admin
from animais import models
from django.utils.html import format_html
from django.urls import reverse
from django.templatetags.static import static
from .forms import AnimalForm
from django.contrib.admin.actions import delete_selected

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
    list_display = 'nome',

@admin.register(models.Animais)
class AnimalAdmin(admin.ModelAdmin):
    inlines = [AnimalImageInline]
    list_display = 'id', 'nome', 'data_nascimento', 'preview', 'acoes', 
    readonly_fields = ['data_nascimento']
    search_fields = ['nome', 'id', 'data_nascimento']
    list_filter = ['especie']
    list_per_page = 10
    ordering = ['-id']
    actions = [delete_selected]
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
        user = getattr(self, 'request', None)
        try:
            request = self.request
        except AttributeError:
            request = None

        change_url = reverse('admin:animais_animais_change', args=[obj.pk])
        delete_url = reverse('admin:animais_animais_delete', args=[obj.pk])
        view_url = reverse('admin:animais_animais_change', args=[obj.pk])
        edit_icon   = static('global/imgs/lapis.png')
        view_icon   = static('global/imgs/olho-admin.png')
        delete_icon = static('global/imgs/x.png')

        parts = []
        if request is None or self.has_change_permission(request, obj):
            parts.append(
                format_html(
                    '<a href="{}"><img class="action-icon" src="{}" '
                    'alt="Editar" title="Editar"/></a>',
                    change_url, edit_icon
                )
            )
        else:
            parts.append(
                format_html(
                    '<a href="{}"><img class="action-icon" src="{}" '
                    'alt="Editar" title="Visualizar"/></a>',
                    view_url, view_icon
                )
            )

        if request is None or self.has_delete_permission(request, obj):
            parts.append(
                format_html(
                    '<a href="{}"><img class="action-icon" src="{}" '
                    'alt="Excluir" title="Excluir"/></a>',
                    delete_url, delete_icon
                )
            )
        return format_html(' '.join(parts))
    acoes.short_description = 'Ações'

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)
    
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        extra_context['app_list'] = list(self.admin_site.get_app_list(request))
        return super().changelist_view(request, extra_context=extra_context)