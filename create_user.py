import os
import django
import random
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sos4patas.settings')
django.setup()

from animais.models import Animais, tipoAnimal

nomes = ['Luna', 'Thor', 'Mel', 'Bob', 'Nina', 'Rex', 'Bela', 'Toby', 'Lola', 'Max']
sexos = ['Fêmea', 'Macho']
portes = ['Pequeno', 'Médio', 'Grande']
especies = ['Cachorro', 'Gato']

tipo = tipoAnimal.objects.first()

for i in range(20):
    idade_anos = random.randint(0, 10)
    idade_meses = random.randint(0, 11)
    data_nascimento = date.today() - relativedelta(years=idade_anos, months=idade_meses)

    animal = Animais(
        nome=nomes[i],
        sexo=random.choice(sexos),
        porte=random.choice(portes),
        especie=random.choice(especies),
        descricao=f"Animal gerado automaticamente para testes ({i})",
        tipo_animal=tipo,
        disponivel_para_adocao=True,
        data_nascimento=data_nascimento
    )
    animal.foto.save(f"teste_{i}.jpg", ContentFile(b"imagem fake"), save=False)
    animal.save()
