from django.db.models import signals
from django.dispatch import receiver
from .models import Product, ProductAttachment
from .utils import *


@receiver(signals.post_save, sender=Product)
def product_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_name(instance, save=True)


def pre_save_change_status_inventory_quantity(instance, sender, **kwargs) :
    if instance.inventory_quantity > 0 :
        instance.is_available = True
    else :
        instance.is_available = False


signals.pre_save.connect(pre_save_change_status_inventory_quantity, sender=ProductAttachment)