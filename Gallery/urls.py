from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterUser, ProtectedUser

urlpatterns = [
    path('register/',RegisterUser.as_view(), name = 'register'),
    path('Login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name = 'refresh'),
    path('profile/', ProtectedUser.as_view(), name = 'profile')
]
