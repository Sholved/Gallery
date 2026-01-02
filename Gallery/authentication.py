from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .utils.jwt import verify_access_token

User = get_user_model()

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return None
        
        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Invalid Authorization header")
        try:
            token = auth_header.split(" ", 1)[1]
        except IndexError:
            raise AuthenticationFailed("Invalid Authorization Header Format")
        
        user_id = verify_access_token(token)
        try:
            user = User.objects.get(id = user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User Does Not Exist") 
        
        return (user, token)