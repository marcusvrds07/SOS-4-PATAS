import os
import sys
import django
import random
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.files import File

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sos4patas.settings')
django.setup()

from animais.models import Animais, TipoAnimal

nomes = ['Luna', 'Thor', 'Mel', 'Bob', 'Nina', 'Rex', 'Bela', 'Toby', 'Lola', 'Max']
sexos = ['Fêmea', 'Macho']
portes = ['Pequeno', 'Médio', 'Grande']
racas = ['Cachorro', 'Gato']

caminho_imagens = 'base_statics/home/img/pack_de_cachorros' 
imagens_disponiveis = os.listdir(caminho_imagens)

tipos = list(TipoAnimal.objects.values_list('nome', flat=True))

qtd = 0
while True:
    qtd = int(input('Digite um número de 1-10 para quantidade de animais que deseja gerar: '))
    if 1 <= qtd <= 10:
        break

print("Raças disponíveis:", ", ".join(racas))

while True:
    escolha_tipo = input("Escolha um tipo (digite exatamente): ").strip()
    if escolha_tipo in tipos:
        tipo = TipoAnimal.objects.get(nome=escolha_tipo)
        break

for i in range(qtd):
    idade_anos = random.randint(0, 10)
    idade_meses = random.randint(0, 11)
    data_nascimento = date.today() - relativedelta(years=idade_anos, months=idade_meses)

    animal = Animais(
        nome=nomes[i],
        sexo=random.choice(sexos),
        porte=random.choice(portes),
        raca=random.choice(racas),
        descricao=f"Animal gerado automaticamente para testes ({i})",
        especie=tipo,
        disponivel_para_adocao=True,
        data_nascimento=data_nascimento
    )

    imagem_nome = random.choice(imagens_disponiveis)
    caminho_imagem = os.path.join(caminho_imagens, imagem_nome)
    with open(caminho_imagem, 'rb') as img:
        animal.foto.save(imagem_nome, File(img), save=False)

    animal.save()
