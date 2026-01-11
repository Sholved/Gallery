from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Image, Album

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta():
        model = User
        fields = ['username', 'email', 'password']
        
    def create(self, validated_data):
        user = User.objects.create_user(
        username = validated_data["username"],
        email = validated_data["email"],
        password = validated_data["password"]
        )
        return user



class ImageSerializer(serializers.ModelSerializer):
    class Meta():
        model = Image
        fields = ['title','id','storage_path','created_at']
        
        read_only_fields = ['id','storage_path', 'created_at']
        
        
class AlbumSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Image.objects.all(),
        required=False
    )
    
    class Meta:
        model = Album
        fields = ["id", "title", "description", "is_public","images", "created_at"]
        read_only_fields = ["id", "created_at"]
    