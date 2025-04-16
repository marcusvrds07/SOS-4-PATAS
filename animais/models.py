from django.db import models
import os

# Create your models here.

def animal_image_upload_path(instance, filename):
    animal = instance.animal_fk
    folder_name = f"ID_{animal.id}"
    return os.path.join('galeria', folder_name, filename)

def capa_upload_path(instance, filename):
    return os.path.join('foto_capa', str(instance.id), filename)

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
    foto = models.ImageField(upload_to=capa_upload_path, null=True)

    # Salva foto com o id(pk) do animal e mantém o nome original
    def save(self, *args, **kwargs):
        if not self.pk and self.foto:
            # Guarda a imagem e remove temporariamente
            foto_temp = self.foto
            self.foto = None
            super().save(*args, **kwargs)  # Salva sem imagem pra gerar o ID

            self.foto = foto_temp  # Restaura a imagem
        super().save(*args, **kwargs)  # Salva com imagem agora que já tem ID
        
    def __str__(self):
        return self.nome
    
class AnimalImage(models.Model):
    animal_fk = models.ForeignKey(Animais, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=animal_image_upload_path)

    def __str__(self):
        return f"Imagem extra de (ID {self.animal_fk.id})"
    
    def delete(self, *args, **kwargs):
    # Remove o arquivo da pasta antes de deletar o objeto
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)