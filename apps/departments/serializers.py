from rest_framework import serializers
from .models import Department,StaffDepartmentAssignment
from accounts.models import User

class DepartmentSerializer(serializers.ModelSerializer):
	staff_count =serializers.ReadOnlyField()
	head_name =serializers.SerializerMethodField()
	head_role=serializers.SerializerMethodField()

	class Meta:
		model=Department
		fields=[
			'id','name','code','description','head','head_name','head_role','is_active','staff_count','created_at',
		]
		read_only_fields=['id','created_at']
	def get_head_name(self,obj):
		return obj.head.full_name if obj.head else None
	def get_head_role(self,obj):
		return obj.head.get_role_display() if obj.head else None

class StaffDepartmentAssignmentSerializer(serializers.ModelSerializer):
	user_name=serializers.SerializerMethodField()
	user_email=serializers.SerializerMethodField()
	user_role=serializers.SerializerMethodField()
	department_name=serializers.SerializerMethodField()
	department_code=serializers.SerializerMethodField()

	class Meta:
		model=StaffDepartmentAssignment
		fields=['id','user','user_name','user_email','user_role','department','department_name','department_code','role_in_department','assigned_on','assigned_until','is_active','notes',
		  ]
		read_only_fields=['id','assigned_on']

	def get_user_name(self,obj):       return obj.user.full_name
	def get_user_email(self,obj):      return obj.user.email
	def get_user_role(self,obj):       return obj.user.get_role_display ()
	def get_department_name(self,obj): return obj.department.name
	def get_department_code(self,obj): return obj.department.code

class DepartmentStaffSerializer (serializers.ModelSerializer):
	role_display =serializers.SerializerMethodField()
	assignment_type=serializers.SerializerMethodField()

	class Meta:
		model=User
		fields= ['id','full_name','email','role','role_display','is_active','date_joined','assignment_type']
	def get_role_display(self,obj):
		return obj.get_role_display()
	def get_assignment_type(self,obj):
		dept=self.context.get('department')
		if not dept:
			return None
		assignment=obj.staff_assignments.filter(department=dept,is_active=True).first()
		return assignment.role_in_dept if assignment else None
