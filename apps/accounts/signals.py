from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.dispatch import receiver
from .models import LoginAuditLog
from django.db.models.functions import Now

@receiver(user_logged_in)
def track_login(sender,user,request,**kwargs):
    x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
    ip=x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    LoginAuditLog.objects.filter(
        user=user,
        is_active_session=True
    ).update(is_active_session=False)
    
    LoginAuditLog.objects.create(
        user=user,
        ip_address=ip,
        user_agent=request.META.get('HTTP_USER_AGENT'),
        is_active_session=True
    )

@receiver(user_logged_out)
def track_logout(sender,user,request,**kwargs):
    if user:
        LoginAuditLog.objects.filter(user=user,is_active_session=True).update(is_active_session=False,logout_time=Now())
