from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterUser, ProtectedUser, UploadImageView, ImageViewSet

router = DefaultRouter()
router.register("images", ImageViewSet, basename = "images")

urlpatterns = [
    path('register/',RegisterUser.as_view(), name = 'register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name = 'refresh'),
    path('profile/', ProtectedUser.as_view(), name = 'profile'),
    path('upload/', UploadImageView.as_view(), name = 'upload'),
]
