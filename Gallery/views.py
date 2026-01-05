from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import RegisterSerializer, ImageSerializer
from .models import Image
from .upload import upload_image

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
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        raise PermissionDenied("Use the upload endpoint to uplod images")