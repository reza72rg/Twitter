from twitter.models import Post
from rest_framework import serializers
from django.contrib.auth.models import User
from twitter.models import Profile, Like, DisLike

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'author','archive']

class UserSerializers(serializers.ModelSerializer):
    posts_author = PostSerializers(read_only= True, many= True)
    
    class Meta:
        model = Profile
        fields = ['user','posts_author']
        
class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post']

class DislikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = DisLike
        fields = ['user', 'post']
