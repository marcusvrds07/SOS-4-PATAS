from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
import os, time
from django.core.files.storage import default_storage
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


def safe_remove(path):
    try:
        time.sleep(0.1)
        try:
            f = default_storage.open(path)
            f.close()
        except:
            pass
        full = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.isfile(full):
            os.remove(full)
    except Exception as e:
        print(f"[ERRO] ao remover {path}: {e}")

@receiver(pre_save, sender=Profile)
def store_old_profile_photo(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Profile.objects.get(pk=instance.pk)
        instance._old_foto = old.foto.name
    except Profile.DoesNotExist:
        instance._old_foto = None

@receiver(post_save, sender=Profile)
def delete_old_profile_photo(sender, instance, **kwargs):
    old = getattr(instance, '_old_foto', None)
    new = instance.foto.name
    if old and old != new:
        safe_remove(old)

@receiver(post_delete, sender=Profile)
def delete_profile_folder(sender, instance, **kwargs):
    folder = os.path.join(settings.MEDIA_ROOT, 'usuarios', str(instance.user.id))
    if os.path.isdir(folder):
        try:
            import shutil
            shutil.rmtree(folder)
        except Exception as e:
            print(f"[ERRO] ao remover pasta {folder}: {e}")
