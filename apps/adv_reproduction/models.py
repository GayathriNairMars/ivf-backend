from django.db import models
from django.utils.text import slugify
from django.conf import settings

class ReproductiveEndocrinologistProfile(models.Model):
	user=models.OneToOneField(to=settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='endocrinologist_profile')
	employee_id=models.CharField(max_length=20,unique=True,null=True,blank=True,help_text='END001')
	slug=models.SlugField(unique=True,null=True)

	specialization=models.CharField(max_length=100,default="Reproductive Endocrinology & Infertility")
	medical_license_no=models.CharField(max_length=50,blank=True)
	years_of_experience=models.PositiveIntegerField(default=0)
	biography=models.TextField(blank=True,null=True)

	can_perform_egg_retrieval=models.BooleanField(default=True)
	can_perform_embryo_transfer=models.BooleanField(default=True)
	can_design_ivf_protocols=models.BooleanField(default=True)
	is_department_head=models.BooleanField(default=True)

	is_active=models.BooleanField(default=True)
	date_assigned=models.DateField(auto_now_add=True)

	def save(self,*args,**kwargs):
		if not self.employee_id:
			last_profile=ReproductiveEndocrinologistProfile.objects.order_by('-id').first()
			if not last_profile:
				self.employee_id="EN001"
			else:
				last_id=int(last_profile.employee_id.replace("EN",""))
				new_id=last_id+1
				self.employee_id= f"EN{new_id:03d}"
		if not self.slug:
			base_slug=slugify(self.user.full_name)
			self.slug=f"{base_slug}-{self.employee_id.lower()}"
		super().save(*args,**kwargs)
	
	def __str__(self):
		return f"Dr. {self.user.full_name} (Reproductive Endocrinologist)"
