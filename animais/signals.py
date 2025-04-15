from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os
import time
from .models import Animais, AnimalImage

def safe_remove(path):
    try:
        time.sleep(0.2)
        if os.path.isfile(path):
            os.remove(path)
    except Exception as e:
        print(f"[ERRO] Ao remover {path}: {e}")

# === FOTO CAPA ===
@receiver(pre_save, sender=Animais)
def delete_old_capa_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    
    try:
        old_instance = Animais.objects.get(pk=instance.pk)
    except Animais.DoesNotExist:
        return

    if old_instance.foto and old_instance.foto != instance.foto:
        safe_remove(old_instance.foto.path)

@receiver(pre_delete, sender=Animais)
def delete_all_images_on_animal_delete(sender, instance, **kwargs):
    if instance.foto and os.path.isfile(instance.foto.path):
        safe_remove(instance.foto.path)

    for image in instance.images.all():
        if image.image and os.path.isfile(image.image.path):
            safe_remove(image.image.path)

# === IMAGENS DA GALERIA ===
@receiver(pre_save, sender=AnimalImage)
def delete_old_gallery_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    
    try:
        old_instance = AnimalImage.objects.get(pk=instance.pk)
    except AnimalImage.DoesNotExist:
        return

    if old_instance.image and old_instance.image != instance.image:
        safe_remove(old_instance.image.path)

@receiver(pre_delete, sender=AnimalImage)
def delete_gallery_image_on_delete(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        safe_remove(instance.image.path)
