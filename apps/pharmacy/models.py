from django.db import models
from django.conf import settings

class PharmacistProfile(models.Model):
    user=models.OneToOneField(to=settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='pharmacist_profile')
    employee_id=models.CharField(max_length=20,unique=True, blank=True,help_text='PH001')
    # slug=models.SlugField(unique=True)


    license_number=models.CharField(max_length=50, blank=True)
    qualification=models.CharField(max_length=100, blank=True)
    store_location=models.CharField(max_length=55, blank=True, help_text='First Floor')
    
    can_manage_inventory=models.BooleanField(default=False)
    is_department_head=models.BooleanField(default=False)

    is_active=models.BooleanField(default=True)
    date_assigned=models.DateField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.employee_id:
            last_profile = PharmacistProfile.objects.order_by('-id').first()
            if not last_profile:
                self.employee_id = "PH001"
            else:
                last_id = int(last_profile.employee_id.replace("PH", ""))
                new_id = last_id + 1
                self.employee_id = f"PH{new_id:03d}"
        super().save(*args,**kwargs)
    def __str__(self):
        return f"Pharmacist {self.user.full_name} "
