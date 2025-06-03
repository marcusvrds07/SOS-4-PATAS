from django.contrib import admin, messages
from animais import models
from django.utils.html import format_html
from django.urls import reverse
from django.templatetags.static import static
from .forms import AnimalForm, TipoAnimalForm
from django.contrib.admin.actions import delete_selected
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib import admin
from .models import AnimaisAdotados



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
    change_list_template = "admin/animais/animais/change_list.html"
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
        if obj is not None and not request.user.has_perm('animais.change_animais'):
            fields = [f.name for f in self.model._meta.fields]
            m2m    = [f.name for f in self.model._meta.many_to_many]
            return fields + m2m
        return super().get_readonly_fields(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return (
                request.user.has_perm('animais.add_animais') or
                request.user.has_perm('animais.change_animais')
            )
        return request.user.has_perm('animais.change_animais')

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
        mark_adopted_icon = static('global/imgs/check.png')

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
                    '<a href="{}"><img class="action-icon" src="{}"  '
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
            parts.append(
                format_html(
                    '''
                    <button type="button"
                        class="mark-adopted-btn"
                        data-id="{id}" 
                        data-nome="{nome}"
                        data-especie="{especie}"
                        data-idade="{idade}"
                        title="Marcar como Adotado"
                        style="margin-left: -25px; background: none; border: none;">
                        <img src="{icon}" class="btn-marcar-adotado" alt="Marcar como Adotado" style="cursor:pointer;" />
                    </button>
                    ''',
                    id=obj.pk,
                    nome=obj.nome,
                    especie=obj.especie,
                    idade=getattr(obj, "idade", "Não informado"),
                    icon=mark_adopted_icon
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

class AnimaisAdotadosForm(forms.ModelForm):
    class Meta:
        model = AnimaisAdotados
        fields = '__all__'
        widgets = {
            'endereco_adotante': forms.TextInput(attrs={'size': '60'}),
        }

@admin.register(models.AnimaisAdotados)
class AnimaisAdotadosAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'data_adocao', 'preview', 'acoes']

    def acoes(self, obj):
        change_url = reverse('admin:animais_animaisadotados_change', args=[obj.pk])
        delete_icon = static('global/imgs/x.png')
        edit_icon = static('global/imgs/lapis.png')

        parts = [
            format_html('<a href="{}"><img src="{}" alt="Editar" title="Editar"/></a>', change_url, edit_icon),
            format_html(
                '<button type="button" class="delete-btn" data-id="{}" data-name="{}">'
                '<img src="{}" alt="Excluir" title="Excluir"/></button>',
                obj.pk, obj.nome, delete_icon
            ),
        ]
        return format_html(' '.join(parts))

    acoes.short_description = 'Ações'

    form = AnimaisAdotadosForm

    change_list_template = "admin/animais/animaisAdotados/change_list.html"
    change_form_template = "admin/animais/animaisAdotados/change_form.html"
    list_display = ['id', 'nome', 'data_adocao', 'preview', 'acoes']
    search_fields = ['nome']
    readonly_fields = ['data_adocao', 'data_nascimento']
    list_per_page = 10
    ordering = ['-data_adocao']

    def preview(self, obj):
        if obj.foto:
            try:
                return format_html(f'<img src="{obj.foto.url}" width="55" style="object-fit:contain;" />')
            except ValueError:
                return "Imagem não encontrada"
        return "-"
    preview.short_description = "Foto da Capa"

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
        ('Informações do Adotante', {
            'fields': (
                'nome_adotante',
                'telefone_adotante',
                'email_adotante',
                'endereco_adotante',
            ),
        }),
        ('Status da Adoção', {
            'fields': ('data_adocao',),
        }),
    )

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['app_list'] = list(self.admin_site.get_app_list(request))
        return super().changelist_view(request, extra_context=extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['app_list'] = list(self.admin_site.get_app_list(request))
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)


