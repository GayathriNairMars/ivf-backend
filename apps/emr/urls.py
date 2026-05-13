from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientEMRViewset

router=DefaultRouter()
router.register(r'',PatientEMRViewset,basename='emr')

urlpatterns= [
	path('',include(router.urls)),
]
