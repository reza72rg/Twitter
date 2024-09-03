from django.db import models
from accounts.models import Profile
from blog.models import Post
from django.urls import reverse


# Create your models here.


class Comment(models.Model):
    author = models.ForeignKey(
        Profile, related_name="user_comment", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, related_name="post_comment", on_delete=models.CASCADE
    )
    content = models.TextField()
    approach = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author} comments in {self.post}"

    def get_snippet(self):
        return self.content[0:5]

    def get_absolute_url(self):
        return reverse("comment:api-v1:comment-detail", kwargs={"pk": self.pk})
