from django.db import models
import os
from datetime import date
from dateutil.relativedelta import relativedelta

# Sessão: caminhos de upload
def animal_image_upload_path(instance, filename):
    return os.path.join('galeria', f'ID_{instance.animal_fk.id}', filename)

def capa_upload_path(instance, filename):
    return os.path.join('foto_capa', str(instance.id), filename)

def adopted_capa_upload_path(instance, filename):
    return os.path.join('animaladotado', 'foto_da_capa', str(instance.id), filename)

def adopted_gallery_upload_path(instance, filename):
    return os.path.join('animaladotado', 'galeria', f'ID_{instance.animal_fk.id}', filename)


# Sessão: modelos de animais e imagens
class TipoAnimal(models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Categoria do Animal"
        verbose_name_plural = 'Categorias dos Animais'

    def __str__(self):
        return self.nome


class Animais(models.Model):

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = 'Animais'

    foto = models.ImageField(upload_to=capa_upload_path)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(blank=True, null=True)
    sexo = models.CharField(choices=[('Fêmea','Fêmea'),('Macho','Macho')])
    porte = models.CharField(choices=[('Pequeno','Pequeno'),('Médio','Médio'),('Grande','Grande')])
    raca = models.CharField(max_length=30)
    especie = models.ForeignKey(TipoAnimal, on_delete=models.SET_NULL, null=True)
    disponivel_para_adocao = models.BooleanField(default=True)
    descricao = models.TextField(blank=True)
    idade_anos = models.PositiveIntegerField(blank=True, null=True)
    idade_meses = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.idade_anos is not None or self.idade_meses is not None:
            anos  = self.idade_anos or 0
            meses = self.idade_meses or 0
            if anos or meses:
                self.data_nascimento = date.today() - relativedelta(years=anos, months=meses)
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
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)


# Sessão: modelos para animais adotados e imagens de adotados
class AnimaisAdotados(models.Model):
    class Meta:
        verbose_name = "Animal Adotado"
        verbose_name_plural = 'Animais Adotados'

    foto = models.ImageField(upload_to=adopted_capa_upload_path)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(blank=True, null=True)
    sexo = models.CharField(choices=[('Fêmea','Fêmea'),('Macho','Macho')])
    porte = models.CharField(choices=[('Pequeno','Pequeno'),('Médio','Médio'),('Grande','Grande')])
    raca = models.CharField(max_length=30)
    especie = models.ForeignKey(TipoAnimal, on_delete=models.SET_NULL, null=True)
    adotado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class AnimalImageAdotado(models.Model):
    animal_fk = models.ForeignKey(AnimaisAdotados, related_name='images_adotado', on_delete=models.CASCADE)
    image     = models.ImageField(upload_to=adopted_gallery_upload_path)

    def __str__(self):
        return f"Imagem adotado (ID {self.animal_fk.id})"

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)


# Sessão: modelos de adotantes e adoções
class Adoptante(models.Model):
    class Meta:
        verbose_name = "Adotante"
        verbose_name_plural = 'Adotantes'

    cpf = models.CharField('CPF', max_length=11, unique=True)
    nome = models.CharField('Nome', max_length=100)
    email = models.EmailField('Email')
    telefone = models.CharField('Telefone', max_length=20)
    endereco = models.TextField('Endereço')

    def __str__(self):
        return f'{self.nome} ({self.cpf})'


class Adocao(models.Model):
    class Meta:
        verbose_name = "Adoção"
        verbose_name_plural = 'Adoções'
    adoptante  = models.ForeignKey(Adoptante, related_name='adocoes', on_delete=models.CASCADE)
    animal     = models.ForeignKey(AnimaisAdotados, related_name='adocoes', on_delete=models.CASCADE)
    data_adocao = models.DateTimeField(auto_now_add=True)