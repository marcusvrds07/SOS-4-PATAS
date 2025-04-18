# Generated by Django 5.2 on 2025-04-14 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('idade', models.IntegerField()),
                ('porte', models.CharField(choices=[('Pequeno', 'Pequeno'), ('Médio', 'Médio'), ('Grande', 'Grande')], max_length=20)),
                ('especie', models.CharField(max_length=30)),
                ('descricao', models.TextField(blank=True)),
                ('disponivel_para_adocao', models.BooleanField(default=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos_animais/')),
            ],
        ),
    ]
