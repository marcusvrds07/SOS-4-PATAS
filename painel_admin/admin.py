from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.templatetags.static import static
from django.utils.html import format_html
from .models import Profile
from .forms import UserProfileCreationForm, UserProfileChangeForm
from django.db import transaction
from django.core.exceptions import PermissionDenied

def delete_selected(modeladmin, request, queryset):
    # Só permite deleção se for superuser
    if not request.user.is_superuser:
        raise PermissionDenied("Apenas superusuários podem excluir usuários.")
    # Não permite auto-exclusão
    if queryset.filter(pk=request.user.pk).exists():
        raise PermissionDenied("Você não pode se excluir.")
    queryset.delete()

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
        # Se não for superuser:
        if not request.user.is_superuser:
            # Só redireciona para admin se NÃO clicou em "continuar editando" ou "adicionar outro"
            if "_continue" not in request.POST and "_addanother" not in request.POST:
                return HttpResponseRedirect(reverse('admin:index'))
            # Se clicou em continuar/adicionar outro, segue o fluxo padrão (fica na edição)
            return super().response_change(request, obj)
        # Se for superuser, segue o fluxo normal (vai pra lista de usuários)
        if "_continue" not in request.POST and "_addanother" not in request.POST:
            if request.user.has_perm("auth.view_user"):
                return HttpResponseRedirect(reverse("admin:auth_user_changelist"))
            else:
                return HttpResponseRedirect(reverse("admin:index"))
        return super().response_change(request, obj)

    # Permissão para adicionar
    def has_add_permission(self, request):
        return request.user.is_superuser

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.pk)

    # Permissão para editar
    def has_change_permission(self, request, obj=None):
        # Superuser pode tudo
        if request.user.is_superuser:
            return True
        # Só pode editar a si mesmo
        if obj is not None and obj == request.user:
            return True
        return False

    # Permissão para deletar
    def has_delete_permission(self, request, obj=None):
        # Só superuser pode excluir e não pode se auto-excluir
        if not request.user.is_superuser:
            return False
        if obj is not None and obj == request.user:
            return False
        return True
    
    # Restringe edição de campo "is_superuser"
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Só desabilita para não superuser
        if not request.user.is_superuser:
            if 'cargo' in form.base_fields:
                form.base_fields['cargo'].disabled = True
            if obj == request.user:
                if 'is_superuser' in form.base_fields:
                    form.base_fields['is_superuser'].disabled = True
        else:
            # Superuser pode editar tudo, nunca desabilite os campos para ele
            if 'cargo' in form.base_fields:
                form.base_fields['cargo'].disabled = False
            if 'is_superuser' in form.base_fields:
                form.base_fields['is_superuser'].disabled = False
        return form
    
    def changelist_view(self, request, extra_context=None):
        # Só superuser acessa a lista. Usuário comum é redirecionado para o dashboard do admin.
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

    # Evita auto-exclusão pelo painel
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