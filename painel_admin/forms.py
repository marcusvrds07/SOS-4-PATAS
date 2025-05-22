from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.models import Group, Permission


class UserProfileCreationForm(UserCreationForm):
    foto = forms.ImageField(required=False, label='Foto de Perfil')
    is_staff = forms.BooleanField(required=False, label='Staff')
    is_active = forms.BooleanField(required=False, label='Ativo')
    is_superuser = forms.BooleanField(required=False, label='Superusuário')
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)
    user_permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'password1', 'password2',
            'is_staff', 'is_active', 'is_superuser',
            'groups', 'user_permissions',
            'foto'
        )

    def save(self, commit=True):
        user = super().save(commit)
        foto = self.cleaned_data.get('foto')
        if commit:
            profile, created = Profile.objects.get_or_create(user=user)
            if foto:
                profile.foto = foto
                profile.save()
        return user

class UserProfileChangeForm(UserChangeForm):
    foto = forms.ImageField(required=False, label='Foto de Perfil')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'foto')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            try:
                profile = self.instance.profile
                self.fields['foto'].initial = profile.foto
            except Profile.DoesNotExist:
                pass

    def save(self, commit=True):
        user = super().save(commit)
        foto = self.cleaned_data.get('foto')
        if commit:
            profile, created = Profile.objects.get_or_create(user=user)
            if foto:
                profile.foto = foto
                profile.save()
        return user
