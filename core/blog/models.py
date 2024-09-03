from django.db import models
from django.urls import reverse
from accounts.models import Profile
from core.tools import UploadToPathAndRename
from accounts.models import MainModel

# from comment.models import Comment


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Post(MainModel):
    content = models.TextField()
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="posts_author"
    )
    image = models.ImageField(
        upload_to=UploadToPathAndRename("posts"),
        default="posts/default.jpg",
    )
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    archive = models.BooleanField(default=True)

    @property
    def likes(self):
        return Like.objects.filter(post=self).count()

    @property
    def dislikes(self):
        return DisLike.objects.filter(post=self).count()

    def __str__(self):
        return self.content[:15]

    def get_snippet(self):
        return self.content[0:5]

    def get_absolute_url(self):
        return reverse("blog:api-v1:task-detail", kwargs={"pk": self.pk})


class Like(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="ulike"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="upost"
    )

    def __str__(self):
        return (
            f"{self.user} --> Like this post -->  {self.post.content[:5]}"
        )


class DisLike(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="udislike"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="udispost"
    )

    def __str__(self):
        return f"{self.user} --> Dislike this post -->  {self.post.content[:5]}"


class ImageFiled(MainModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=UploadToPathAndRename("posts"),
        default="posts/default.jpg",
    )

    def __str__(self):
        return self.post
