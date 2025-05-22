<div align="center">
  <br>
  <img src="base_statics/global/imgs/logoazul.png" width="180" alt="Logo SOS 4 PATAS" style="margin-bottom:16px;"/>
  <p>
    <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/marcusvrds07/SOS-4-PATAS?color=1954cb">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/marcusvrds07/SOS-4-PATAS?color=1954cb">
    <img alt="License" src="https://img.shields.io/github/license/marcusvrds07/SOS-4-PATAS?color=1954cb">
  </p>
  <br>
</div>

---

## 🌎 Veja Online

> [**Acesse a aplicação aqui**](https://link-sera-adicionado-em-breve.com)  
> *(Adicionaremos o link em breve!)*

---

## 🚀 Sobre

Esta aplicação foi desenvolvida para a **ONG SOS 4 PATAS**, dedicada ao resgate, proteção e adoção de animais.  
O sistema oferece ferramentas administrativas modernas para cadastro, atualização, filtragem e organização dos dados dos animais e usuários, além de funcionalidades para voluntários e gerenciamento interno da ONG.

---

## 📋 Funcionalidades

- Cadastro e gerenciamento de animais (inclusão, edição, exclusão, filtros e busca)
- Gerenciamento de usuários e permissões administrativas
- Gestão de voluntários
- Painel administrativo responsivo e customizado
- Página pública com informações sobre a ONG

---

## ⚙️ Tecnologias Utilizadas

- ![Django](https://img.shields.io/badge/-Django-092E20?style=flat&logo=django&logoColor=white) **Django 5.2**
- ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white) **Python 3**
- ![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat&logo=html5&logoColor=white) **HTML5**
- ![CSS3](https://img.shields.io/badge/-CSS3-1572B6?style=flat&logo=css3&logoColor=white) **CSS3**
- ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) **JavaScript**
- ![SQLite](https://img.shields.io/badge/-SQLite-003B57?style=flat&logo=sqlite&logoColor=white) **SQLite**

---

## 💻 Como rodar localmente

```bash
# Clone o repositório
git clone https://github.com/marcusvrds07/SOS-4-PATAS.git
cd SOS-4-PATAS

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Rode o servidor local
python manage.py runserver
