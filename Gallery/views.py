from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer

User = get_user_model()

class RegisterUser(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    

class ProtectedUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
     
    def get(self, request):
        return Response(f'Hello, {request.user.username}, You are Authenticated')

    
    
# class ReminderList(generics.ListCreateAPIView):
#     serializer_class = ReminderSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         return Reminder.objects.filter(user = self.request.user)
    
#     def perform_create(self, serializer):
#         return serializer.save(user = self.request.user)