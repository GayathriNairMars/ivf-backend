from rest_framework.permissions import BasePermission

class AppointmentPermissions(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser or request.user.role == "ADM":
            return True
        
        if view.action in ["list","create","onboard","dashboard",'my_profile']:
            return request.user.role == "REC"
        return False

