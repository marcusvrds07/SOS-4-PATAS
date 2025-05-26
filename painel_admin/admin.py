from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.templatetags.static import static
from django.utils.html import format_html
from .models import Profile
from .forms import UserProfileCreationForm, UserProfileChangeForm
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

def delete_selected(modeladmin, request, queryset):
    if not request.user.is_superuser:
        raise PermissionDenied("Apenas superusuários podem excluir usuários.")
    if queryset.filter(pk=request.user.pk).exists():
        raise PermissionDenied("Você não pode se excluir.")
    queryset.delete()

admin.site.unregister(Group)

class CustomGroupAdmin(BaseGroupAdmin):
    list_display = ('name', 'acoes',)
    search_fields = ('name',)
    ordering = ('name',)
    fields = ('name', 'permissions')
    filter_horizontal = ('permissions',)  

    def get_list_display(self, request):
        self._current_request = request
        return super().get_list_display(request)
    
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

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "permissions":
            kwargs["queryset"] = Permission.objects.exclude(
                codename__in=[
                    "delete_logentry",
                    "view_logentry",
                    "change_logentry",
                    "add_logentry",
                    "add_animalimage",
                    "change_animalimage",
                    "delete_animalimage",
                    "view_animalimage",
                    "view_group",
                    "change_group",
                    "add_group",
                    "delete_group",
                    "add_user",
                    "delete_user",
                    "change_user",
                    "view_user",
                    "view_permission",
                    "delete_permission",
                    "change_permission",
                    "add_permission",
                    "add_contenttype",
                    "delete_contenttype",
                    "change_contenttype",
                    "view_contenttype",
                    "view_profile",
                    "change_profile",
                    "add_profile",
                    "delete_profile",
                    "delete_session",
                    "change_session",
                    "view_session",
                    "add_session",
                ]
            )
            field = super().formfield_for_manytomany(db_field, request, **kwargs)

            action_map = {
                "add": _("Adicionar"),
                "change": _("Alterar"),
                "delete": _("Excluir"),
                "view": _("Visualizar"),
            }
            def label_from_instance(obj):
                verb = obj.codename.split("_")[0]
                return f"{action_map.get(verb, verb)} {obj.content_type.name}"
            field.label_from_instance = label_from_instance

            return field

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def acoes(self, obj):
        request = getattr(self, '_current_request', None)
        if not request or not request.user.is_superuser:
            return '-'

        change_url = reverse('admin:auth_group_change', args=[obj.pk])
        delete_url = reverse('admin:auth_group_delete', args=[obj.pk])
        view_url = change_url

        edit_icon = static('global/imgs/lapis.png')
        delete_icon = static('global/imgs/x.png')

        parts = [
            format_html(
                '<a href="{}"><img class="action-icon" src="{}" alt="Editar" title="Editar"/></a>',
                change_url, edit_icon
            ),
            format_html(
                '<a href="{}"><img class="action-icon" src="{}" alt="Excluir" title="Excluir"/></a>',
                delete_url, delete_icon
            ),
        ]
        return format_html(' '.join(parts))

    acoes.short_description = 'Ações'
    acoes.allow_tags = True


class CustomUserAdmin(BaseUserAdmin):
    actions = [delete_selected]
    list_display = ('username', 'email', 'first_name', 'last_name', 'acoes')
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_filter = ['is_active', 'groups']
    filter_horizontal = ['user_permissions', 'groups']
    readonly_fields = ('date_joined', 'last_login')

    add_form = UserProfileCreationForm
    form = UserProfileChangeForm

    add_fieldsets = (
        ('Perfil', {'fields': ('foto',)}),
        ('Informações básicas', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'cargo'),
        }),
        ('Senha e Confirmação de Senha', {
            'fields': ('password1', 'password2')
        }),
    )
    fieldsets = (
        ('Perfil', {'fields': ('foto',)}),
        ('Login e Senha', {'fields': ('username', 'password',)}),
        ('Informações básicas', {
            'fields': ('email', 'first_name', 'last_name', 'cargo'),
            'classes': ('wide',),
        }),
        ('Permissões', {'fields': ('is_superuser',)}),
        ('Datas', {'fields': ('date_joined', 'last_login'),}),
    )

    def response_change(self, request, obj):
        if not request.user.is_superuser:
            if "_continue" not in request.POST and "_addanother" not in request.POST:
                return HttpResponseRedirect(reverse('admin:index'))
            return super().response_change(request, obj)
        if "_continue" not in request.POST and "_addanother" not in request.POST:
            if request.user.has_perm("auth.view_user"):
                return HttpResponseRedirect(reverse("admin:auth_user_changelist"))
            else:
                return HttpResponseRedirect(reverse("admin:index"))
        return super().response_change(request, obj)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.pk)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        if obj is not None and obj == request.user:
            return False
        return True
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'cargo' in form.base_fields:
                form.base_fields['cargo'].disabled = True
            if obj == request.user:
                if 'is_superuser' in form.base_fields:
                    form.base_fields['is_superuser'].disabled = True
        else:
            if 'cargo' in form.base_fields:
                form.base_fields['cargo'].disabled = False
            if 'is_superuser' in form.base_fields:
                form.base_fields['is_superuser'].disabled = False
        return form
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['app_list'] = list(self.admin_site.get_app_list(request))
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['app_list'] = list(self.admin_site.get_app_list(request))
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('admin:index'))
        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            cargo = form.cleaned_data.get('cargo')
            super().save_model(request, obj, form, change)
            obj.groups.clear()
            if cargo:
                obj.groups.add(cargo)
            foto = form.cleaned_data.get('foto')
            profile, created = Profile.objects.get_or_create(user=obj)
            if foto:
                profile.foto = foto
                profile.save()

    def delete_model(self, request, obj):
        if obj == request.user:
            raise PermissionDenied("Você não pode se excluir.")
        super().delete_model(request, obj)

    def acoes(self, obj):
        request = self._current_request
        change_url = reverse('admin:auth_user_change', args=[obj.pk])
        delete_url = reverse('admin:auth_user_delete', args=[obj.pk])
        view_url = change_url

        edit_icon = static('global/imgs/lapis.png')
        view_icon = static('global/imgs/olho-admin.png')
        delete_icon = static('global/imgs/x.png')
        parts = []

        if self.has_change_permission(request, obj):
            parts.append(
                format_html('<a href="{}"><img class="action-icon" src="{}" alt="Editar" title="Editar"/></a>', change_url, edit_icon)
            )
        elif self.has_view_permission(request, obj):
            parts.append(
                format_html('<a href="{}"><img class="action-icon" src="{}" alt="Visualizar" title="Visualizar"/></a>', view_url, view_icon)
            )

        if self.has_delete_permission(request, obj):
            parts.append(
                format_html(
                    '<button type="button" class="delete-btn" data-id="{}" data-name="{}">'
                    '<img class="action-icon" src="{}" alt="Excluir" title="Excluir"/>'
                    '</button>',
                    obj.pk, obj.username, delete_icon
                )
            )
        return format_html(' '.join(parts)) if parts else '-'

    acoes.short_description = 'Ações'
    acoes.allow_tags = True

    def get_list_display(self, request):
        self._current_request = request
        return super().get_list_display(request)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)