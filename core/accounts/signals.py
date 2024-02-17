from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import Profile
from twitter.models import Post


@receiver(post_save, sender=Profile)
def update_profile(sender, instance, created, **kwargs):
    if not instance.active:
        posts = Post.objects.filter(author= instance.user.profile)
        for post in posts:
            post.archive = False
            post.save()
