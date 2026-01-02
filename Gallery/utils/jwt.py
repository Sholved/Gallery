import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY,
            algorithms=["HS256"],
            options={"require": ["exp", "user_id"]}
        )
    except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Has Expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Token is invalid')
    
    user_id = payload.get("user_id")
    if not user_id:
        raise AuthenticationFailed('Invalid Token payload')
    
    return user_id
