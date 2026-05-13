from rest_framework.permissions import BasePermission

class StaffPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True
        #ADMIN role permissions
        if request.user.is_staff:
            return True
        #HR Manager role permissions
        if view.action in ["list","create","onboard","dashboard","my_profile",'hr_permissions','toggle_status','rec_permissions','audit-log']:
            return request.user.role == "HRM"
        if view.action in [""]:
            return 
        return False