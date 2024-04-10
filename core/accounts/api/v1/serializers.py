from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Follow, Profile
from rest_framework.exceptions import ValidationError


class UserSerializers(serializers.ModelSerializer):
    #posts_author = PostSerializers(read_only= True, many= True)
    #user_comment = CommentSerializers(read_only= True, many= True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Profile
        fields = ['id','username', 'email', 'active', 'descriptions']


class UserTestSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Profile
        fields = ['id','username']
   
  

    
    
class FollowersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'user', 'follow_user', 'date']
        read_only_fields = ['user']
       
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["user"] = UserTestSerializers(instance.user).data
        rep["follow_user"] = UserTestSerializers(instance.follow_user).data
        return rep   
    
    def create(self, validated_data):          
        validated_data['user'] = Profile.objects.get(user__id = self.context.get('request').user.id)    
        if validated_data['follow_user'] != validated_data['user']:
            return super().create(validated_data)
   
   
    def create(self, validated_data):          
        validated_data['user'] = Profile.objects.get(user__id=self.context.get('request').user.id) 
        relation = Follow.objects.filter(user=validated_data['user'], follow_user=validated_data['follow_user'])   
        if validated_data['follow_user'] == validated_data['user']:
            raise ValidationError({"error": "You cannot follow yourself."}, code='invalid')
        elif relation.exists():
            raise ValidationError({"error": "You cannot follow this user again."}, code='invalid')
        
        
        
        
        return super().create(validated_data)
    
