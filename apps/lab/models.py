from django.db import models
from  django.conf import settings

class LabTechnicianProfile(models.Model):
    user=models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='technician_profile')
    employee_id=models.CharField(max_length=20,unique=True, blank=True,help_text='LT001')
    # slug=models.SlugField(unique=True)

    technical_certification=models.CharField(max_length=250, blank=True)
    specialization=models.CharField(max_length=50, blank=True)

    is_department_head=models.BooleanField(default=False)

    is_active=models.BooleanField(default=True)
    date_assigned=models.DateField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.employee_id:
            last_profile = LabTechnicianProfile.objects.order_by('-id').first()
            if not last_profile:
                self.employee_id = "LT001"
            else:
                last_id = int(last_profile.employee_id.replace("LT", ""))
                new_id = last_id + 1
                self.employee_id = f"LT{new_id:03d}"
        super().save(*args,**kwargs)
    def __str__(self):
        return f"Lab-Technician: {self.user.full_name}"

class AndrologyLabTechnician(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="andrology_technician_profile")
    employee_id=models.CharField(max_length=20,unique=True,blank=True,help_text='AT001')
    
    technician_license=models.CharField(max_length=100,unique=True,blank=True)
    specialization=models.CharField(max_length=50,blank=True)

    can_perform_dna_frag = models.BooleanField(default=False,help_text="Authorized for Sperm DNA Fragmentation Indexing")
    can_perform_cryo = models.BooleanField(default=True, help_text="Authorized to freeze and map semen samples")
    is_department_head=models.BooleanField(default=False)

    is_active=models.BooleanField(default=True)
    date_assigned=models.DateField(auto_now_add=True)

    def save(self,request,*args,**kwargs):
        if not self.employee_id:
            last_profile=AndrologyLabTechnician.objects.order_by('-id').first()
            if not last_profile:
                self.employee_id=f"AT001"
            else:
                last_id=int(last_profile.employee_id.replace("AT",""))
                new_id=last_id+1
                self.employee_id=f"AT{new_id:03d}"
        super().save(*args,**kwargs)
    def __str__(self):
        return f"Andrology Lab-Technician: {self.user.full_name}"


