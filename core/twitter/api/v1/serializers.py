from twitter.models import Post
from rest_framework import serializers
from django.contrib.auth.models import User
from twitter.models import Profile, Like, DisLike, Comment

class CommentSerializers(serializers.ModelSerializer):   
    snippet = serializers.CharField(source = 'get_snippet',  read_only= True)
    relative_url = serializers.URLField(source= 'get_absolute_url', read_only= True)
    absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'snippet','relative_url','absolute_url' ,'approach' ,'author']
        read_only_fields = ['author']
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('snippet')
            rep.pop('absolute_url')
            rep.pop('relative_url')
            
        else:

            rep.pop('content')
        rep["author"] = UserSerializers(instance.author,).data
        return rep
    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user__id = self.context.get('request').user.id)
        return super().create(validated_data)
    def get_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
class UserSerializers(serializers.ModelSerializer):
    #posts_author = PostSerializers(read_only= True, many= True)
    #user_comment = CommentSerializers(read_only= True, many= True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    snippet = serializers.CharField( source = 'get_snippet', read_only= True)
    absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['id','username', 'email', 'active', 'descriptions','snippet','absolute_url']
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('snippet')
            rep.pop('absolute_url')
        else:
            rep.pop('descriptions')
            rep.pop('email')
            
        return rep
    def get_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
     
class PostSerializers(serializers.ModelSerializer):
    snippet = serializers.CharField( source = 'get_snippet', read_only= True)
    relative_url = serializers.URLField( source= 'get_absolute_url', read_only= True)
    absolute_url = serializers.SerializerMethodField()
    # author = serializers.SlugRelatedField(
    #     many=False, slug_field="user.username", queryset=Profile.objects.all()
    # )
    
    class Meta:
        model = Post
        fields = ['id', 'content', 'snippet','relative_url','absolute_url', 'archive','author']
        read_only_fields = ['author']
   
    def get_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('snippet')
            rep.pop('absolute_url')
            rep.pop('relative_url')
        else:
            rep.pop('content')
        rep["author"] = UserSerializers(
            instance.author, context={"request": request}
        ).data
        return rep
    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user__id = self.context.get('request').user.id)
        return super().create(validated_data)
    

class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post','user']
        read_only_fields = ['user']
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["user"] = UserSerializers(
            instance.user).data
        return rep
    def create(self, validated_data):
        validated_data['user'] = Profile.objects.get(user__id = self.context.get('request').user.id)
        return super().create(validated_data)


class DislikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = DisLike
        fields = ['id', 'post','user']
        read_only_fields = ['user']
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["user"] = UserSerializers(
            instance.user).data
        return rep
    def create(self, validated_data):
        validated_data['user'] = Profile.objects.get(user__id = self.context.get('request').user.id)
        return super().create(validated_data)
