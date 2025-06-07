from django.db.models.signals import pre_delete, pre_save, post_save,post_delete
from django.conf import settings
from django.dispatch import receiver
import os, gc
import time
import shutil
from .models import Animais, AnimalImage

def safe_remove(path):
    try:
        time.sleep(0.2)
        try:
            from django.core.files.storage import default_storage
            file = default_storage.open(path)
            file.close()
        except Exception:
            pass
        
        if os.path.isfile(path):
            os.remove(path)
    except Exception as e:
        print(f"[ERRO] Ao remover {path}: {e}")

#FOTO CAPA:
 
@receiver(pre_save, sender=Animais)
def store_old_capa_before_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_instance = Animais.objects.get(pk=instance.pk)
        instance._old_foto = old_instance.foto
    except Animais.DoesNotExist:
        instance._old_foto = None


@receiver(post_save, sender=Animais)
def delete_old_capa_after_change(sender, instance, **kwargs):
    old_foto = getattr(instance, '_old_foto', None)
    if old_foto and old_foto.name != instance.foto.name:
        try:
            if hasattr(old_foto, 'close'):
                old_foto.close()
        except Exception as e:
            print(f"[ERRO] Ao fechar imagem antiga: {e}")
        safe_remove(old_foto.path)

@receiver(post_delete, sender=Animais)
def delete_animal_folder(sender, instance, **kwargs):
    folder_path = os.path.join(settings.MEDIA_ROOT, 'foto_capa', str(instance.pk))
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"[OK] Pasta {folder_path} removida com sucesso.")
        except Exception as e:
            print(f"[ERRO] Ao remover pasta: {e}")


# GALERIA: 

@receiver(pre_delete, sender=Animais)
def delete_all_images_on_animal_delete(sender, instance, **kwargs):
    if instance.foto and os.path.isfile(instance.foto.path):
        safe_remove(instance.foto.path)

    for image in instance.images.all():
        if image.image and os.path.isfile(image.image.path):
            safe_remove(image.image.path)

    folder_path = os.path.join('media', 'galeria', f'ID_{instance.id}')
    if os.path.isdir(folder_path):
        try:
            shutil.rmtree(folder_path)
        except Exception as e:
            print(f"[ERRO] Ao remover pasta {folder_path}: {e}")

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