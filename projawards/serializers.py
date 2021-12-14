from rest_framework import serializers
from .models import Profile, Post
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'photo','description', 'url', 'technologies_used', 'upload_date', 'user']
        
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','name', 'profile_pic', 'bio', 'phone_number']


