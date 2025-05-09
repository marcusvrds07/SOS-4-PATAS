import os
import django
import random
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sos4patas.settings')
django.setup()

from animais.models import Animais, tipoAnimal

nomes = ['Luna', 'Thor', 'Mel', 'Bob', 'Nina', 'Rex', 'Bela', 'Toby', 'Lola', 'Max']
sexos = ['Fêmea', 'Macho']
portes = ['Pequeno', 'Médio', 'Grande']
especies = ['Cachorro', 'Gato']

caminho_imagens = 'base_statics/home/img/pack_de_cachorros' 
imagens_disponiveis = os.listdir(caminho_imagens)


escolha_tipo = input('tipo animal: ')
tipo = tipoAnimal.objects.get(tipo_animal=escolha_tipo)

for i in range(10):
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

    imagem_nome = random.choice(imagens_disponiveis)
    caminho_imagem = os.path.join(caminho_imagens, imagem_nome)
    with open(caminho_imagem, 'rb') as img:
        animal.foto.save(imagem_nome, File(img), save=False)

    animal.save()
