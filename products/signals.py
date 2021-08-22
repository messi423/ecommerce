from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from users.models import Profile


def create_order(sender, instance, created, **kwargs):
    if created:
        Order.objects.create(owner=instance.user.username)


def save_order_profile(sender, instance, **kwargs):
    post_save.connect(create_order, sender=User)
