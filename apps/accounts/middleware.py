from django.shortcuts import redirect
from django.urls import reverse

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response=get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            exempt_urls= [
                reverse('staff-force-password-change'),
                reverse('logout'),
            ]
            has_changed=getattr(request.user,'has_changed_password',True)
            if not has_changed and request.path not in exempt_urls:
                target_url=request.get_full_path()
                login_url=reverse('staff-force-password-change')
                return redirect(f'{login_url}?next={target_url}')
        return self.get_response(request)
    