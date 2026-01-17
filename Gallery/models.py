from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from uuid import uuid4

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
class Image(models.Model):
    id = models.UUIDField(primary_key= True, default=uuid4, editable= False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add=True)
    storage_path = models.CharField(max_length=512, null = True)
    is_public = models.BooleanField(default = False)
    
    def __str__(self):
        return self.title
    
class Album(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="albums"
        )
    title = models.CharField(max_length=255)
    description = models.TextField(blank = True)
    images = models.ManyToManyField("Image", related_name="albums", blank = True)

    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
         return f"{self.title} ({self.owner})"

    
"https://dtiqleetduadxhqemuby.supabase.co"
"sb_secret_LucIh5qSil6SUZqFiMLXmQ_6kr0sXi0"