from django.contrib import admin, messages
from django.core.files.base import ContentFile

from animais import models
from django.utils.html import format_html
from django.urls import reverse
from django.templatetags.static import static
from .forms import AnimalForm, TipoAnimalForm
from django.contrib.admin.actions import delete_selected
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib import admin
from .models import AnimaisAdotados, TipoAnimal
from django.http import HttpResponseRedirect
from django.urls import path
from datetime import datetime, timedelta
from django.utils import timezone
from os.path import basename



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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(disponivel_para_adocao=True)

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

    class Media:
        js = (
            'js/change_list.js',
            'js/change_list_adotados.js',
        )

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
        revert_icon = static('global/imgs/reverter.png')

        # revert_url = reverse('admin:reverter_para_disponivel', args=[obj.pk])

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
            mark_adopted_url = reverse('admin:marcar_como_adotado', args=[obj.pk])

            parts.append(
                format_html(
                    '<a href="#" title="Marcar como Adotado" class="marked-button" data-url="{}">'
                    '<img src="{}" class="btn-marcar-adotado action-icon" style="cursor:pointer;" alt="Marcar como Adotado" /></a>',
                    mark_adopted_url,
                    mark_adopted_icon
                )
            )

        return format_html(' '.join(parts))
    acoes.short_description = 'Ações'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                'marcar_como_adotado/<int:animal_id>/',
                self.admin_site.admin_view(self.marcar_como_adotado),
                name='marcar_como_adotado',
            ),
        ]
        return custom_urls + urls

    def marcar_como_adotado(self, request, animal_id):
        from .models import Animais, AnimaisAdotados

        try:
            animal = Animais.objects.get(pk=animal_id)
        except Animais.DoesNotExist:
            self.message_user(request, "Animal não encontrado.", level=messages.ERROR)
            return HttpResponseRedirect(reverse('admin:animais_animais_changelist'))

        # Cria o registro do animal adotado com os dados do animal
        novo_adotado = AnimaisAdotados.objects.create(
            animal_original_id=animal.id,
            nome=animal.nome,
            sexo=animal.sexo,
            porte=animal.porte,
            raca=animal.raca,
            especie=animal.especie,
            descricao=animal.descricao or '',
            idade_anos=getattr(animal, 'idade_anos', None),
            idade_meses=getattr(animal, 'idade_meses', None),
            data_nascimento=animal.data_nascimento,
        )

        # Copia a foto, se existir, e salva corretamente
        if animal.foto:
            nome_arq = basename(animal.foto.name)
            with animal.foto.open('rb') as f:
                novo_adotado.foto.save(nome_arq, ContentFile(f.read()), save=True)
            animal.foto.delete(save=False)

        self.message_user(request, f'O animal "{animal.nome}" foi marcado como adotado.')

        # Deleta o animal original (opcional, mas geralmente desejado)
        animal.delete()

        # Redireciona para a página de edição do animal adotado recém-criado
        return HttpResponseRedirect(
            reverse('admin:animais_animaisadotados_change', args=[novo_adotado.pk])
        )

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

from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse, path
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect

@admin.register(models.AnimaisAdotados)
class AnimaisAdotadosAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'data_adocao', 'preview', 'acoes']
    readonly_fields = ['data_adocao', 'data_nascimento']
    search_fields = ['nome']
    list_per_page = 10
    ordering = ['-data_adocao']
    form = AnimaisAdotadosForm

    change_list_template = "admin/animais/animaisAdotados/change_list.html"
    change_form_template = "admin/animais/animaisAdotados/change_form.html"

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

    def preview(self, obj):
        if obj.foto:
            try:
                return format_html(
                    '<img src="{}" width="55" style="object-fit: contain;" />',
                    obj.foto.url
                )
            except ValueError:
                return "Imagem não encontrada"
        return "-"
    preview.short_description = "Foto da Capa"

    def acoes(self, obj):
        change_url = reverse('admin:animais_animaisadotados_change', args=[obj.pk])
        delete_icon = static('global/imgs/x.png')
        edit_icon = static('global/imgs/lapis.png')
        reverse_icon = static('global/imgs/refazer.png')

        reverse_url = reverse('admin:reverter_adocao', args=[obj.pk])

        parts = [
            format_html(
                '<a href="{}"><img src="{}" class="action-icon" alt="Editar" title="Editar"/></a>',
                change_url, edit_icon
            ),
            format_html(
                '<button type="button" class="delete-btn" data-id="{}" data-name="{}">'
                '<img src="{}" alt="Excluir" class="action-icon" title="Excluir"/></button>',
                obj.pk, obj.nome, delete_icon
            ),
            format_html(
                '<a href="#" title="Reverter Adoção" class="revert-button" data-url="{}">'
                '<img src="{}" class="action-icon" alt="Reverter Adoção" /></a>',
                reverse_url, reverse_icon
            )
        ]
        return format_html(' '.join(parts))
    acoes.short_description = 'Ações'

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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'reverter_adocao/<int:adotado_id>/',
                self.admin_site.admin_view(self.reverter_adocao),
                name='reverter_adocao',
            ),
        ]
        return custom_urls + urls

    def reverter_adocao(self, request, adotado_id):
        try:
            adotado = models.AnimaisAdotados.objects.get(pk=adotado_id)
        except models.AnimaisAdotados.DoesNotExist:
            self.message_user(request, "Registro de animal adotado não encontrado.", level=messages.ERROR)
            return HttpResponseRedirect(reverse('admin:animais_animaisadotados_changelist'))

        try:
            tipo_animal = TipoAnimal.objects.get(nome=adotado.especie)
        except TipoAnimal.DoesNotExist:
            tipo_animal = None  # ou criar: TipoAnimal.objects.create(nome=adotado.especie)

        novo_animal = models.Animais.objects.create(
            nome=adotado.nome,
            sexo=adotado.sexo,
            porte=adotado.porte,
            raca=adotado.raca,
            especie=tipo_animal,
            descricao=adotado.descricao,
            idade_anos=getattr(adotado, 'idade_anos', None),
            idade_meses=getattr(adotado, 'idade_meses', None),
            data_nascimento=adotado.data_nascimento,
            disponivel_para_adocao=True,
        )

        if adotado.foto:
            nome_arquivo = basename(adotado.foto.name)
            caminho = adotado.foto.name
            if not default_storage.exists(caminho):
                caminho = f'foto_capa_adotado/{adotado.id}/{nome_arquivo}'
            with default_storage.open(caminho, 'rb') as f:
                novo_animal.foto.save(nome_arquivo, ContentFile(f.read()), save=True)
            adotado.foto.delete(save=False)

        novo_animal.save()
        adotado.delete()

        self.message_user(request, f'A adoção do animal "{novo_animal.nome}" foi revertida com sucesso.')
        return HttpResponseRedirect(reverse('admin:animais_animais_change', args=[novo_animal.pk]))
