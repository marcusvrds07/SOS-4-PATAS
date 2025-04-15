import os
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import Animais

# Deletar a foto ao deletar o animal
@receiver(pre_delete, sender=Animais)
def delete_animal_image_on_delete(sender, instance, **kwargs):
    if instance.foto and os.path.isfile(instance.foto.path):
        os.remove(instance.foto.path)

# ubstituir a foto ao atualizar
@receiver(pre_save, sender=Animais)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = Animais.objects.get(pk=instance.pk)
    except Animais.DoesNotExist:
        return

    old_file = old_instance.foto
    new_file = instance.foto

    # se a imagem foi trocada ou removida
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
