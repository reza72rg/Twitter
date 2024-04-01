from twitter.models import Post
from rest_framework import serializers
from django.contrib.auth.models import User
from twitter.models import Profile, Like, DisLike, Comment

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'author','archive']

class UserSerializers(serializers.ModelSerializer):
    posts_author = PostSerializers(read_only= True, many= True)
    
    class Meta:
        model = Profile
        fields = ['id','user','posts_author']
        
class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id','user', 'post']

class DislikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = DisLike
        fields = ['id','user', 'post']

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','author', 'post', 'content', 'approach']
