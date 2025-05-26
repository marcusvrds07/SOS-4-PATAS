from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.models import Group, Permission


class UserProfileCreationForm(UserCreationForm):
    foto = forms.ImageField(required=False, label='Foto de Perfil')
    user_permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required=False)
    cargo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        empty_label="Selecione um cargo",
        label="Cargo"
    )
    is_staff = forms.BooleanField(required=False, label='Staff')
    is_active = forms.BooleanField(required=False, label='Ativo')
    is_superuser = forms.BooleanField(required=False, label='Superusuário')

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'cargo',
            'password1', 'password2',
            'is_staff', 'is_active', 'is_superuser',
            'groups', 'user_permissions',
            'foto'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        cargo = self.cleaned_data.get('cargo')
        user.is_staff = True
        user.is_active = True

        if commit:
            user.save()
            if cargo:
                user.groups.set([cargo])
            foto = self.cleaned_data.get('foto')
            profile, created = Profile.objects.get_or_create(user=user)
            if foto:
                profile.foto = foto
                profile.save()
        return user

class UserProfileChangeForm(UserChangeForm):
    foto = forms.ImageField(required=False, label='Foto de Perfil')
    cargo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        empty_label="Selecione um cargo",
        label="Cargo"
    )

    class Meta:
            model = User
            fields = (
                'username', 'email', 'first_name', 'last_name', 'cargo',
                'is_staff', 'is_active', 'is_superuser',
                'groups', 'foto'
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            grupos = self.instance.groups.all()
            if grupos.exists():
                self.fields['cargo'].initial = grupos.first()
            try:
                profile = self.instance.profile
                self.fields['foto'].initial = profile.foto
            except Profile.DoesNotExist:
                pass

    def save(self, commit=True):
        user = super().save(commit=False)
        cargo = self.cleaned_data.get('cargo')
        user.is_staff = True

        if commit:
            user.save()
            if cargo:
                user.groups.set([cargo])
            foto = self.cleaned_data.get('foto')
            profile, created = Profile.objects.get_or_create(user=user)
            if foto:
                profile.foto = foto
                profile.save()
        return user