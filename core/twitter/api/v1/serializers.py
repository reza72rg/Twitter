from twitter.models import Post
from rest_framework import serializers
from django.contrib.auth.models import User
from twitter.models import Profile, Like, DisLike, Comment

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','author', 'post', 'content', 'approach']

class PostSerializers(serializers.ModelSerializer):
    snippet = serializers.CharField( source = 'get_snippet', read_only= True)
    relative_url = serializers.URLField( source= 'get_absolute_url', read_only= True)
 
   
    
    class Meta:
        model = Post
        fields = ['id', 'content','author', 'snippet','relative_url', 'archive']
   
class UserSerializers(serializers.ModelSerializer):
    posts_author = PostSerializers(read_only= True, many= True)
    user_comment = CommentSerializers(read_only= True, many= True)
    class Meta:
        model = Profile
        fields = ['id','user','posts_author','user_comment']
        
class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id','user', 'post']

class DislikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = DisLike
        fields = ['id','user', 'post']
