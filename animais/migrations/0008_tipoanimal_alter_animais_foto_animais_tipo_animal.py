# Generated by Django 5.2 on 2025-04-17 16:22

import animais.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animais', '0007_rename_animal_animalimage_animal_fk'),
    ]

    operations = [
        migrations.CreateModel(
            name='tipoAnimal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_animal', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='animais',
            name='foto',
            field=models.ImageField(upload_to=animais.models.capa_upload_path),
        ),
        migrations.AddField(
            model_name='animais',
            name='tipo_animal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='animais.tipoanimal'),
        ),
    ]
