from itertools import product
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Product


@receiver(post_save, sender=Order)
def del_products(sender, instance, created, update_fields,  **kwargs):
    if created:
        update = Product.objects.get(name = instance.product)
        update.number_in_contract = update.number_in_contract - instance.quantity
        update.save()




    