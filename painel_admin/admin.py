from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.templatetags.static import static
from django.utils.html import format_html
from .models import Profile
from .forms import UserProfileCreationForm, UserProfileChangeForm

def delete_selected(modeladmin, request, queryset):
    queryset.delete()

class CustomUserAdmin(BaseUserAdmin):
    actions = [delete_selected]
    list_display = ('username', 'email', 'first_name', 'last_name', 'acoes')
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_filter = ['is_staff', 'is_superuser', 'is_active']

    add_form = UserProfileCreationForm
    form = UserProfileChangeForm

    add_fieldsets = (
        ('Informações básicas', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
        ('Perfil', {
            'fields': ('foto',),
        }),
    )


    fieldsets = BaseUserAdmin.fieldsets + (
        ('Perfil', {'fields': ('foto',)}),
    )

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = self.add_form
        else:
            kwargs['form'] = self.form
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        foto = form.cleaned_data.get('foto')
        profile, created = Profile.objects.get_or_create(user=obj)
        if foto:
            profile.foto = foto
            profile.save()

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

    def acoes(self, obj):
        request = self._current_request
        change_url = reverse('admin:auth_user_change', args=[obj.pk])
        delete_url = reverse('admin:auth_user_delete', args=[obj.pk])
        view_url   = change_url

        edit_icon   = static('global/imgs/lapis.png')
        view_icon   = static('global/imgs/olho-admin.png')
        delete_icon = static('global/imgs/x.png')

        parts = []

        if self.has_change_permission(request, obj):
            parts.append(
                format_html(
                    '<a href="{}"><img class="action-icon" src="{}" alt="Editar" title="Editar"/></a>',
                    change_url, edit_icon
                )
            )
        elif self.has_view_permission(request, obj):
            parts.append(
                format_html(
                    '<a href="{}"><img class="action-icon" src="{}" alt="Visualizar" title="Visualizar"/></a>',
                    view_url, view_icon
                )
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
