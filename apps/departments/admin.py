from django.contrib import admin
from .models import Department,StaffDepartmentAssignment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
	list_display=['name','code','head','is_active','staff_count','created_at']
	list_filter=['is_active']
	search_fields=['name','code']

@admin.register(StaffDepartmentAssignment)
class StaffDepartmentAssignmentAdmin(admin.ModelAdmin):
	list_display=['user','department','role_in_dept','is_active','assigned_on','assigned_until']
	list_filter=['role_in_dept','is_active','department']
	search_fields=['user__full_name','user__email','department__name']
	raw_id_fields=['user','department']
