from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import RegisterSerializer, ImageSerializer, AlbumSerializer
from .models import Image, Album
from .upload import upload_image, delete_image
from .permissions import PublicReadOnly, IsOwner

User = get_user_model()

class RegisterUser(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    

class ProtectedUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
     
    def get(self, request):
        return Response(f'Hello, {request.user.username}, You are Authenticated')


class UploadImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        file = request.FILES.get("image")
        title = request.data.get("title")
        
        if not file:
            return Response({"error": "No file provided"}, status=400)
        
        image = Image.objects.create(
            owner=request.user,
            title = title
        )
        try:
            path = upload_image(file, request.user, image.id)
            image.storage_path = path
            image.save()
        except Exception:
            image.delete()
            return Response({"error": "Image upload failed"}, status = 500)
        
        
        return Response({
            "id": str(image.id),
            "path": image.storage_path}, status= 201)
        
        
class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated, PublicReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        return Image.objects.filter(
            Q(owner=user) | Q(is_public = True)
        )  
    
    def perform_create(self, serializer):
        raise PermissionDenied("Use the upload endpoint to uplod images")
    
    def destroy(self, request, *args, **kwargs):
        image = self.get_object()
        
        if image.storage_path:
            delete_image(image.storage_path)
            
        image.delete()
        return Response(
            {"messages": "Image deleted successfully"}, 
            status= status.HTTP_204_NO_CONTENT
        )
        
class PublicImageView(ListAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Image.objects.filter(is_public = True)
    
class AlbumView(ModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.action == "list":
            return Album.objects.filter(owner = user)
        return Album.objects.filter(owner = user)
    
    def perform_create(self, serializer):
        serializer.save(owner = self.request.owner)
        
    def perform_update(self, serializer):
        album = self.get_object()
        
        images = serializer.validated_data.get("images", [])
        
        for image in images:
            if image.owner != self.requested.owner:
                raise PermissionDenied("You can only add your images")
            
        serializer.save()