from twitter.models import Post
from rest_framework import serializers
from django.contrib.auth.models import User
from twitter.models import Profile

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'author']

class UserSerializers(serializers.ModelSerializer):
    posts_author = PostSerializers(read_only= True, many= True)
    
    class Meta:
        model = Profile
        fields = ['user','posts_author']