from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Post


@receiver(post_delete, sender=Post, dispatch_uid="delete")
def object_post_delete_handler(sender, instance, **kwargs):
    cache.clear()


@receiver(post_save, sender=Post, dispatch_uid="create-posts")
def object_post_save_handler(sender, instance, **kwargs):
    cache.clear()
