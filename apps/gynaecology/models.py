from django.db import models
from django.utils.text import slugify
from django.conf import settings

class GynaecologistProfile(models.Model):
    user=models.OneToOneField(to=settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='gynaec_profile')
    employee_id=models.CharField(max_length=20, unique=True, blank=True,help_text='DR001')
    slug=models.SlugField(unique=True, blank=True)

    specialization=models.CharField(max_length=100, blank=True)
    medical_license_no=models.CharField(max_length=50, blank=True)
    biography=models.TextField(blank=True,null=True)

    #capability
    can_perform_egg_retrieval = models.BooleanField(default=False)
    can_assist_ivf = models.BooleanField(default=False)
    is_department_head=models.BooleanField(default=False)

    is_active=models.BooleanField(default=True)
    date_assigned=models.DateField(auto_now_add=True)
    def save(self,*args,**kwargs):
        if not self.employee_id:
            last_profile = GynaecologistProfile.objects.order_by('-id').first()
            if not last_profile:
                self.employee_id = "DR001"
            else:
                last_id = int(last_profile.employee_id.replace("DR", ""))
                new_id = last_id + 1
                self.employee_id = f"DR{new_id:03d}"
        if not self.slug:
            base_slug = slugify(self.user.full_name)
            self.slug = f"{base_slug}-{self.employee_id.lower()}"
        super().save(*args,**kwargs)

    def __str__(self):
        return f"Dr. {self.user.full_name}(Gynaecologist)"
