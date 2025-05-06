from django.db import models
import os
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

def animal_image_upload_path(instance, filename):
    animal = instance.animal_fk
    folder_name = f"ID_{animal.id}"
    return os.path.join('galeria', folder_name, filename)

def capa_upload_path(instance, filename):
    return os.path.join('foto_capa', str(instance.id), filename)

class tipoAnimal(models.Model):
    
    tipo_animal = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.tipo_animal}'

class Animais(models.Model):
    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = 'Animais'

    nome = models.CharField(max_length=100, help_text='Digite o seu nome')
    anos = models.IntegerField()
    meses = models.IntegerField(validators=[
            MinValueValidator(0),
            MaxValueValidator(11)
        ],
        help_text="Informe a idade em meses (entre 0 e 11)"
    )
    sexo = models.CharField(choices=[('Fêmea', 'Fêmea'), ('Macho', 'Macho')])
    porte = models.CharField(max_length=20, choices=[('Pequeno', 'Pequeno'), ('Médio', 'Médio'), ('Grande', 'Grande')])
    especie = models.CharField(max_length=30)
    descricao = models.TextField(blank=True)
    tipo_animal = models.ForeignKey(tipoAnimal, on_delete=models.SET_NULL, null=True)
    disponivel_para_adocao = models.BooleanField(default=True)
    foto = models.ImageField(upload_to=capa_upload_path)

    def save(self, *args, **kwargs):
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