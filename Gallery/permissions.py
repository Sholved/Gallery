from rest_framework.permissions import BasePermission, SAFE_METHODS

class PublicReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        
        if request.method in SAFE_METHODS and obj.is_public:
            return True
        
        return False
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.owner