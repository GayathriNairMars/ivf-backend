from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ReceptionistView

app_name = 'appointments'

router=DefaultRouter()
router.register(r'receptionist_view', ReceptionistView,basename='receptionist_view')

urlpatterns=[
    path('',include(router.urls))
]
