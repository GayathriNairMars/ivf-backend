from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import StaffManagementViewSet,ClinicLoginView,ClinicLogoutView,CSRFTokenView,MeView
router=DefaultRouter()
router.register(r'staff-management',StaffManagementViewSet,basename='staff')

urlpatterns=[
	path('csrf/',CSRFTokenView.as_view(),name='csrf'),
    path('login/', ClinicLoginView.as_view(), name='login'),
    path('logout/', ClinicLogoutView.as_view(), name='logout'),
    path('me/',MeView.as_view(),name='me'),
    path('',include(router.urls)),
    ]
