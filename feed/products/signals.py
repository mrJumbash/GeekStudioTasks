from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from feed.products.models import Product

@receiver(post_save, sender=Product)
def image_compressor(sender, **kwargs):
    if kwargs["created"]:
        with Image.open(kwargs["instance"].image.path) as photo:
            photo.save(kwargs["instance"].image.path, optimize=True, quality=50)
