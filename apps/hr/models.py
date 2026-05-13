from django.db import models
from django.conf import settings
from django.utils.text import slugify

class HRManagerProfile(models.Model):
    user=models.OneToOneField(to=settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='hr_profile')
    employee_id=models.CharField(max_length=20,unique=True, blank=True,help_text='HR001')
    slug=models.SlugField(unique=True, blank=True)

    managed_depts=models.CharField(max_length=200, null=True, blank=True,help_text="Eg: Clinical, Laboratory,..")
    contact_number=models.CharField(max_length=15,unique=True,blank=True,null=True)

    can_approve_leaves=models.BooleanField(default=True)
    can_view_salaries=models.BooleanField(default=True)
    can_terminate_staff=models.BooleanField(default=False)
    can_edit_attendance=models.BooleanField(default=False)
    can_generate_payslips=models.BooleanField(default=True)
    can_update_documents=models.BooleanField(default=True)
    is_department_head=models.BooleanField(default=False)

    is_active=models.BooleanField(default=True)
    date_assigned=models.DateField(auto_now_add=True)
    def save(self,*args,**kwargs):
        if not self.employee_id:
            last_profile = HRManagerProfile.objects.order_by('-id').first()
            if not last_profile:
                self.employee_id = "HR001"
            else:
                last_id = int(last_profile.employee_id.replace("HR", ""))
                new_id = last_id + 1
                self.employee_id = f"HR{new_id:03d}"
        if not self.slug:
            base_slug = slugify(self.user.full_name)
            self.slug = f"{base_slug}-{self.employee_id.lower()}"
        super().save(*args,**kwargs)
    def __str__(self):
        return f"HR Manager: {self.user.full_name}"
