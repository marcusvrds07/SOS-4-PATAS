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

    # salva foto com o id(pk) do animal.
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        if self.foto:
            ext = os.path.splitext(self.foto.name)[1]
            new_name = f'{self.pk}{ext}'

            if os.path.basename(self.foto.name) != new_name:
                from django.core.files.base import ContentFile
                file_content = self.foto.read()
                self.foto.save(new_name, ContentFile(file_content), save=False)

        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.nome