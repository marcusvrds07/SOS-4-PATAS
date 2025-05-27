from django import forms
from animais.models import Animais, TipoAnimal
from dateutil.relativedelta import relativedelta
from datetime import date
from .models import Adoptante

class CpfForm(forms.Form):
    cpf = forms.CharField(label='CPF', max_length=11)

class AdoptanteForm(forms.ModelForm):
    class Meta:
        model = Adoptante
        fields = ['cpf', 'nome', 'email', 'telefone', 'endereco']
        widgets = {
            'cpf': forms.HiddenInput()
        }

class AnimalForm(forms.ModelForm):
    idade_anos = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 100}),
        label="Anos"
    )
    idade_meses = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 100}),
        label="Meses"
    )

    class Meta:
        model = Animais
        fields = '__all__'

    def save(self, commit=True):
        animal = super().save(commit=False)
        animal.idade_anos = self.cleaned_data.get('idade_anos') or 0
        animal.idade_meses = self.cleaned_data.get('idade_meses') or 0
        if commit:
            animal.save()
        return animal

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.data_nascimento:
            delta = relativedelta(date.today(), self.instance.data_nascimento)
            self.fields['idade_anos'].initial = delta.years
            self.fields['idade_meses'].initial = delta.months

    def clean(self):
        cleaned_data = super().clean()
        anos = cleaned_data.get('idade_anos') or 0
        meses = cleaned_data.get('idade_meses') or 0
        if anos > 0 or meses > 0:
            cleaned_data['data_nascimento'] = date.today() - relativedelta(years=anos, months=meses)
        return cleaned_data

class TipoAnimalForm(forms.ModelForm):
    class Meta:
        model = TipoAnimal
        fields = ['nome']
