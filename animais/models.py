from django.db import models
import os
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from dateutil.relativedelta import relativedelta

# Create your models here.

def animal_image_upload_path(instance, filename):
    animal = instance.animal_fk
    folder_name = f"ID_{animal.id}"
    return os.path.join('galeria', folder_name, filename)

def capa_upload_path(instance, filename):
    return os.path.join('foto_capa', str(instance.id), filename)

class TipoAnimal(models.Model):
    class Meta:
        verbose_name = "Categoria do Animal"
        verbose_name_plural = 'Categorias dos Animais'
    
    nome = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.nome}'

class Animais(models.Model):
    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = 'Animais'

    foto = models.ImageField(upload_to=capa_upload_path)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(blank=True, null=True)
    sexo = models.CharField(choices=[('Fêmea', 'Fêmea'), ('Macho', 'Macho')])
    porte = models.CharField(max_length=20, choices=[('Pequeno', 'Pequeno'), ('Médio', 'Médio'), ('Grande', 'Grande')])
    raca = models.CharField(max_length=30)
    especie = models.ForeignKey(TipoAnimal, on_delete=models.SET_NULL, null=True)
    disponivel_para_adocao = models.BooleanField(default=True)
    descricao = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.idade_anos is not None or self.idade_meses is not None:
            if self.idade_anos is None:
                self.idade_anos = 0
            if self.idade_meses is None:
                self.idade_meses = 0
            if self.idade_anos > 0 or self.idade_meses > 0:
                total_idade = relativedelta(years=self.idade_anos, months=self.idade_meses)
                self.data_nascimento = date.today() - total_idade
            else:
                self.data_nascimento = None

        if not self.pk and self.foto:
            foto_temp = self.foto
            self.foto = None
            super().save(*args, **kwargs)
            self.foto = foto_temp
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.nome
    
class AnimalImage(models.Model):
    animal_fk = models.ForeignKey(Animais, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=animal_image_upload_path)

    def __str__(self):
        return f"Imagem extra de (ID {self.animal_fk.id})"
    
    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)