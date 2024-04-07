from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from core.tools import UploadToPathAndRename
from .setting import MainModel



# Profile Model
class Profile(MainModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # Foreign key relation with User model
    first_name = models.CharField(max_length=250, blank=True, null=True)  # First name of the user
    last_name = models.CharField(max_length=250, blank=True, null=True)  # Last name of the user
    image = models.ImageField(upload_to=UploadToPathAndRename("profile"),default='profile/default.jpg'
    )  # Image field for user profile picture
    descriptions = (
        models.TextField(blank=True, null=True)
    )  # Text field for user profile description
    active = models.BooleanField(default= True)
    create_date = models.DateTimeField(
        auto_now_add=True
    )  # Date and time when profile was created
    update_date = models.DateTimeField(
        auto_now=True
    )  # Date and time when profile was last updated

    def __str__(self):
        return self.user.username

    @property
    def followers(self):
        return Follow.objects.filter(follow_user__id=self.user.id).count()

    @property
    def following(self):
        return Follow.objects.filter(user__id=self.user.id).count()
    def get_snippet(self):
        if self.descriptions:
            return self.descriptions[0:5]
        else:
            return f"null"
# Signal to create profile when user is created
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        


class Follow(models.Model):
    user = models.ForeignKey(Profile, related_name='user_follow', on_delete=models.CASCADE)
    follow_user = models.ForeignKey(Profile, related_name='follow_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user} following {self.follow_user}'

