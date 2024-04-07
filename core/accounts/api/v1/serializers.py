from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Follow, Profile
from twitter.api.v1.serializers import UserSerializers

class FollowersSerializers(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(many=False, slug_field="user.username", queryset=Profile.objects.all())
    class Meta:
        model = Follow
        fields = ['id', 'user', 'follow_user', 'username', 'date']
        read_only_fields = ['user']
    
    
   
    def create(self, validated_data):
        validated_data['user'] = Profile.objects.get(user__id = self.context.get('request').user.id)
        return super().create(validated_data)
    
    
