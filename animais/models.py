from django.db import models
import os

# Create your models here.

class Animais(models.Model):
    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = 'Animais'

    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    porte = models.CharField(max_length=20, choices=[('Pequeno', 'Pequeno'), ('Médio', 'Médio'), ('Grande', 'Grande')])
    especie = models.CharField(max_length=30)
    descricao = models.TextField(blank=True)
    disponivel_para_adocao = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='foto_capa/', blank=True, null=True)

    def save(self, *args, **kwargs):
        ext = os.path.splitext(self.foto.name)[1]
        if self.id:
            self.foto.name = f'fotos_animais/{self.id}{ext}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome