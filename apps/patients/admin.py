from django.contrib import admin
from .models import PatientProfile

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
	list_display=['patient_id','user','treatment_type','status','assigned_doctor','registered_on']
	list_filter=['status','treatment_type','gender']
	search_fields=['patient_id','user__full_name','user__email','phone']
	raw_id_fields=['user','assigned_doctor','partner']
