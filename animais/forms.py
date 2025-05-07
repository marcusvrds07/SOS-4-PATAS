from django import forms
from animais.models import Animais

class AnimalForm(forms.ModelForm):
    idade_anos = forms.IntegerField(min_value=0, label="Idade (anos)")
    idade_meses = forms.IntegerField(min_value=0, max_value=11, label="Idade (meses)")

    class Meta:
        model = Animais
        fields = '__all__'

    def save(self, commit=True):
        animal = super().save(commit=False)
        animal.idade_anos = self.cleaned_data['idade_anos']
        animal.idade_meses = self.cleaned_data['idade_meses']
        if commit:
            animal.save()
        return animal