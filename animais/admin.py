from django.contrib import admin, messages
from animais import models
from django.utils.html import format_html
from django.urls import reverse
from django.templatetags.static import static
from .forms import AnimalForm, TipoAnimalForm
from django.contrib.admin.actions import delete_selected
from django.http import HttpResponseRedirect

# Register your models here.

class AnimalImageInline(admin.TabularInline):
    model = models.AnimalImage
    extra = 1
    template = "animais/gallery_inline.html"
    readonly_fields = ['preview']
    fields = ['image']

    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('animais.view_animais')

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('animais.change_animais')

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('animais.change_animais')

    def has_add_permission(self, request, obj=None):
        return request.user.has_perm('animais.change_animais')

    def preview(self, obj):
        if obj.image:
            try:
                return format_html(f'<img src="{obj.image.url}" width="80" style="object-fit:contain;" />')
            except ValueError:
                return "Imagem não encontrada"
        return "-"
    def get_readonly_fields(self, request, obj=None):
        if not request.user.has_perm('animais.change_animais'):
            fields = [f.name for f in self.model._meta.fields]
            m2m = [f.name for f in self.model._meta.many_to_many]
            return fields + m2m
        return super().get_readonly_fields(request, obj)

@admin.register(models.TipoAnimal)
class TipoAnimalAdmin(admin.ModelAdmin):
    actions = [delete_selected]
    list_display = 'nome', 'acoes',
    search_fields = ['nome']
    list_per_page = 10
    form = TipoAnimalForm


    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['app_list'] = list(self.admin_site.get_app_list(request))
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)
    
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['app_list'] = list(self.admin_site.get_app_list(request))
        return super().changelist_view(request, extra_context=extra_context)
    
    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    def acoes(self, obj):
        user = getattr(self, 'request', None)
        try:
            request = self.request
        except AttributeError:
            request = None

        change_url = reverse('admin:animais_tipoanimal_change', args=[obj.pk])
        delete_url = reverse('admin:animais_tipoanimal_delete', args=[obj.pk])
        view_url = reverse('admin:animais_tipoanimal_change', args=[obj.pk])
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
                    '<button type="button" class="delete-btn" data-id="{}" data-name="{}">'
                    '<img class="action-icon" src="{}" alt="Excluir" title="Excluir"/>'
                    '</button>',
                    obj.pk, obj.nome, delete_icon
                )
            )
        return format_html(' '.join(parts))
    acoes.short_description = 'Ações'
    fieldsets = (
            ('Dados da Categoria', {
                'fields': ('nome',),
            }),
    )

@admin.register(models.Animais)
class AnimalAdmin(admin.ModelAdmin):
    actions = [delete_selected]
    inlines = [AnimalImageInline]
    list_display = 'id', 'nome', 'data_nascimento', 'preview', 'acoes', 
    readonly_fields = ['data_nascimento']
    search_fields = ['nome', 'id', 'data_nascimento']
    list_filter = ['especie', 'raca', 'sexo', 'porte']
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

    def get_readonly_fields(self, request, obj=None):
        if not request.user.has_perm('animais.change_animais'):
            fields = [f.name for f in self.model._meta.fields]
            m2m = [f.name for f in self.model._meta.many_to_many]
            return fields + m2m
        return super().get_readonly_fields(request, obj)
    
    def has_change_permission(self, request, obj=None):
        if not request.user.has_perm('animais.change_animais'):
            if request.method in ['POST', 'PUT']:
                return False
        return super().has_change_permission(request, obj)

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
                    '<button type="button" class="delete-btn" data-id="{}" data-name="{}">'
                    '<img class="action-icon" src="{}" alt="Excluir" title="Excluir"/>'
                    '</button>',
                    obj.pk, obj.nome, delete_icon
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
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}

        extra_context['app_list'] = list(self.admin_site.get_app_list(request))
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)
    
    fieldsets = (
        ('Foto de Capa', {
            'fields': ('foto',),
        }),
        ('Dados Básicos', {
            'fields': ('nome', 'sexo', 'porte', 'raca', 'especie'),
        }),
        ('Descrição', {
            'fields': ('descricao',),
        }),
        ('Idade e Nascimento', {
            'fields': ('idade_anos', 'idade_meses', 'data_nascimento'),
        }),
        ('Status', {
            'fields': ('disponivel_para_adocao',),
        }),
    )
