from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Image
from easy_thumbnails.files import get_thumbnailer


@receiver(pre_delete, sender=Image)
def image_pre_delete(sender, instance, **kwargs):
    thumbnailer = get_thumbnailer(instance.file)
    thumbnailer.delete_thumbnails()
    # Also delete the original image file
    instance.file.delete(save=False)