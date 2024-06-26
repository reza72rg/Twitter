from django.db import models
from django.urls import reverse
from accounts.models import  Profile
from core.tools import UploadToPathAndRename
from accounts.models import MainModel

class Post(MainModel):
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete = models.CASCADE , related_name = 'posts_author')
    image = models.ImageField(upload_to=UploadToPathAndRename("posts"),default='posts/default.jpg'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    archive = models.BooleanField(default = True)
    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self,approach = True).count() 
    
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
        return reverse('twitter:api-v1:task-detail', kwargs={'pk':self.pk})

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ulike')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='upost')
    def __str__(self):
        return f'{self.user} --> Like this post -->  {self.post.content[:5]}' 
    
    
class DisLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='udislike')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='udispost')
    def __str__(self):
        return f'{self.user} --> Dislike this post -->  {self.post.content[:5]}' 
    
    
class Comment(models.Model):
    author = models.ForeignKey(Profile, related_name='user_comment', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_comment', on_delete=models.CASCADE)
    content = models.TextField()
    approach = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.author} comments in {self.post}'
    
    def get_snippet(self):
        return self.content[0:5]
    def get_absolute_url(self):
        return reverse('twitter:api-v1:comment-detail', kwargs={'pk':self.pk})
    
class ImageFiled(MainModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=UploadToPathAndRename("posts"),default='posts/default.jpg'
    )
    
    
    def __str__(self):
        return self.post    