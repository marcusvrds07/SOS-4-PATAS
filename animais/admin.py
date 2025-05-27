from django.contrib import admin, messages
from animais import models
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.templatetags.static import static
import os
from django.contrib.admin import site as admin_site
from .forms import AnimalForm, TipoAnimalForm, CpfForm, AdoptanteForm
from django.contrib.admin.actions import delete_selected


class AnimalImageInline(admin.TabularInline):
    model = models.AnimalImage
    extra = 1
    template = "animais/gallery_inline.html"
    readonly_fields = ['preview']
    fields = ['image']

    def preview(self, obj):
        if obj.image:
            try:
                return format_html(f'<img src="{obj.image.url}" width="80" style="object-fit:contain;" />')
            except ValueError:
                return "Imagem não encontrada"
        return "-"

    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('animais.view_animais')
    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('animais.change_animais')
    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('animais.change_animais')
    def has_add_permission(self, request, obj=None):
        return request.user.has_perm('animais.change_animais')

    def get_readonly_fields(self, request, obj=None):
        if not request.user.has_perm('animais.change_animais'):
            fields = [f.name for f in self.model._meta.fields]
            m2m = [f.name for f in self.model._meta.many_to_many]
            return fields + m2m
        return super().get_readonly_fields(request, obj)

class AnimalImageAdotadoInline(admin.TabularInline):
    model = models.AnimalImageAdotado
    extra = 1
    readonly_fields = ['preview']
    fields = ['image']

    def preview(self, obj):
        if obj.image:
            try:
                return format_html(f'<img src="{obj.image.url}" width="80" style="object-fit:contain;" />')
            except ValueError:
                return "Imagem não encontrada"
        return "-"

class AdocaoInline(admin.TabularInline):
    model = models.Adocao
    extra = 0
    can_delete = False
    readonly_fields = ('animal_link', 'data_adocao')
    fields = ('animal_link', 'data_adocao')
    verbose_name = "Animal Adotado"
    verbose_name_plural = "Animais Adotados"

    def animal_link(self, obj):
        url = reverse('admin:animais_animaisadotados_change', args=[obj.animal.pk])
        return format_html('<a href="{}">{}</a>', url, obj.animal.nome)
    animal_link.short_description = 'Animal'

@admin.register(models.TipoAnimal)
class TipoAnimalAdmin(admin.ModelAdmin):
    actions = [delete_selected]
    list_display = ('nome', 'acoes')
    search_fields = ['nome']
    list_per_page = 10
    form = TipoAnimalForm
    fieldsets = (
        ('Dados da Categoria', {'fields': ('nome',)}),
    )

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    def acoes(self, obj):
        request = getattr(self, 'request', None)
        change_url = reverse('admin:animais_tipoanimal_change', args=[obj.pk])
        delete_url = reverse('admin:animais_tipoanimal_delete', args=[obj.pk])
        edit_icon  = static('global/imgs/lapis.png')
        delete_icon= static('global/imgs/x.png')
        parts = []
        if not request or self.has_change_permission(request, obj):
            parts.append(format_html('<a href="{}"><img class="action-icon" src="{}" title="Editar"/></a>', change_url, edit_icon))
        if not request or self.has_delete_permission(request, obj):
            parts.append(format_html(
                '<a href="{}"><img class="action-icon" src="{}" title="Excluir"/></a>',
                delete_url, delete_icon
            ))
        return format_html(' '.join(parts))
    acoes.short_description = 'Ações'

@admin.register(models.AnimaisAdotados)
class AnimaisAdotadosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'data_nascimento', 'sexo', 'porte', 'raca', 'especie', 'adotado_em')
    readonly_fields = ('adotado_em',)
    search_fields = ('nome','raca')
    list_filter = ('especie','sexo','porte')
    list_per_page = 10
    ordering = ['-adotado_em']
    inlines = [AnimalImageAdotadoInline]

@admin.register(models.Adoptante)
class AdoptanteAdmin(admin.ModelAdmin):
    list_display = ('cpf','nome','email','telefone')
    search_fields = ('cpf','nome')
    inlines = [AdocaoInline]
    list_per_page = 10

@admin.register(models.Adocao)
class AdocaoAdmin(admin.ModelAdmin):
    list_display  = ('adoptante','animal','data_adocao')
    search_fields = ('adoptante__cpf','animal__nome')
    list_filter   = ('data_adocao',)
    list_per_page = 10

@admin.register(models.Animais)
class AnimalAdmin(admin.ModelAdmin):
    actions = [delete_selected]
    inlines = [AnimalImageInline]
    list_display = ('id','nome','data_nascimento','preview','acoes')
    readonly_fields = ['data_nascimento']
    search_fields = ['nome','id','data_nascimento']
    list_filter = ['especie','raca','sexo','porte']
    list_per_page = 10
    ordering = ['-id']
    form = AnimalForm

    fieldsets = (
        ('Foto de Capa', {'fields': ('foto',)}),
        ('Dados Básicos', {'fields': ('nome','sexo','porte','raca','especie')}),
        ('Descrição', {'fields': ('descricao',)}),
        ('Idade e Nascimento', {'fields': ('idade_anos','idade_meses','data_nascimento')}),
        ('Status', {'fields': ('disponivel_para_adocao',)}),
    )

    def preview(self, obj):
        if obj.foto:
            try:
                return format_html(f'<img src="{obj.foto.url}" width="55" style="object-fit:contain;" />')
            except ValueError:
                return "Imagem não encontrada"
        return "-"
    preview.short_description = 'Foto da Capa'

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.has_perm('animais.change_animais'):
            fields = [f.name for f in self.model._meta.fields] + [f.name for f in self.model._meta.many_to_many]
            return fields
        return super().get_readonly_fields(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return request.user.has_perm('animais.add_animais') or request.user.has_perm('animais.change_animais')
        return request.user.has_perm('animais.change_animais')

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    def acoes(self, obj):
        request    = getattr(self, 'request', None)
        change_url = reverse('admin:animais_animais_change', args=[obj.pk])
        delete_url = reverse('admin:animais_animais_delete', args=[obj.pk])
        edit_icon  = static('global/imgs/lapis.png')
        delete_icon= static('global/imgs/x.png')
        parts = []
        if not request or self.has_change_permission(request, obj):
            parts.append(format_html('<a href="{}"><img class="action-icon" src="{}" title="Editar"/></a>', change_url, edit_icon))
        if not request or self.has_delete_permission(request, obj):
            parts.append(format_html(
                '<button type="button" class="delete-btn" data-id="{}" data-delete-url="{}">'
                '<img class="action-icon" src="{}" title="Excluir"/></button>',
                obj.pk, reverse('admin:animais_animais_delete', args=[obj.pk]), delete_icon
            ))
        return format_html(' '.join(parts))
    acoes.short_description = 'Ações'

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
        custom = [
            path(
                '<path:object_id>/change/adotar/',
                self.admin_site.admin_view(self.adotar_view),
                name='animais_animais_adotar'
            ),
        ]
        return custom + urls

    def adotar_view(self, request, object_id):
        animal = get_object_or_404(models.Animais, pk=object_id)
        if request.method == 'GET':
            return TemplateResponse(request, 'admin/adotar_modal.html', {
                'step': 'cpf', 'form': CpfForm()
            })

        if 'nome' not in request.POST:
            form = CpfForm(request.POST)
            if form.is_valid():
                cpf = form.cleaned_data['cpf']
                try:
                    adotante = models.Adoptante.objects.get(cpf=cpf)
                    adopted = models.AnimaisAdotados.objects.create(
                        nome=animal.nome,
                        data_nascimento=animal.data_nascimento,
                        sexo=animal.sexo,
                        porte=animal.porte,
                        raca=animal.raca,
                        especie=animal.especie,
                    )
                    adopted.foto.save(os.path.basename(animal.foto.name), animal.foto.file, save=True)
                    for img in animal.images.all():
                        ai = models.AnimalImageAdotado(animal_fk=adopted)
                        ai.image.save(os.path.basename(img.image.name), img.image.file, save=True)
                        ai.save()
                    models.Adocao.objects.create(adoptante=adotante, animal=adopted)
                    animal.delete()
                    messages.success(request, 'Animal adotado com sucesso.')
                    return redirect('..')
                except models.Adoptante.DoesNotExist:
                    return TemplateResponse(request, 'admin/adotar_modal.html', {
                        'step': 'info', 'form': AdoptanteForm(initial={'cpf': cpf})
                    })
            return TemplateResponse(request, 'admin/adotar_modal.html', {
                'step': 'cpf', 'form': form
            })

        form2 = AdoptanteForm(request.POST)
        if form2.is_valid():
            adotante = form2.save()
            adopted = models.AnimaisAdotados.objects.create(
                nome=animal.nome,
                data_nascimento=animal.data_nascimento,
                sexo=animal.sexo,
                porte=animal.porte,
                raca=animal.raca,
                especie=animal.especie,
            )
            adopted.foto.save(os.path.basename(animal.foto.name), animal.foto.file, save=True)
            for img in animal.images.all():
                ai = models.AnimalImageAdotado(animal_fk=adopted)
                ai.image.save(os.path.basename(img.image.name), img.image.file, save=True)
                ai.save()
            models.Adocao.objects.create(adoptante=adotante, animal=adopted)
            animal.delete()
            messages.success(request, 'Animal adotado com sucesso.')
            return redirect('..')

        return TemplateResponse(request, 'admin/adotar_modal.html', {
            'step': 'info', 'form': form2
        })

MODEL_ORDER = [
    'Animais',
    'AnimaisAdotados',
    'Adoptante',
    'Adocao',
    'TipoAnimal',
]

def _reorder_animais(app_list):
    for app in app_list:
        if app['app_label'] == 'animais':
            lookup = {m['object_name']: m for m in app['models']}
            app['models'] = [lookup[n] for n in MODEL_ORDER if n in lookup]
            break
    return app_list

_old_get_app_list = admin_site.get_app_list


def get_app_list(request):
    apps = _old_get_app_list(request)
    return _reorder_animais(apps)

admin_site.get_app_list = get_app_list