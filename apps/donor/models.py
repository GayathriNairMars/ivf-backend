import re
from django.db import models
from django.conf import settings
from django.utils.text import slugify

class DonorProfile(models.Model):
    DONOR_TYPES=[('EGG','Egg Donor'),('SPERM','Sperm Donor'),('EMBRYO','Embryo Donor')]

    donor_code=models.CharField(max_length=10,unique=True, blank=True,editable=False, help_text="eg: DON001")
    donor_type=models.CharField(max_length=20,choices=DONOR_TYPES, blank=True)

    #incase of embryo donor, couple details are required.
    donor_partner=models.OneToOneField(to="self",on_delete=models.SET_NULL,blank=True,null=True,related_name='embryo_donor_partner') 

    date_of_birth=models.DateField(blank=True,null=True)
    blood_group=models.CharField(max_length=5,choices=[('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('O+','O+'),('O-','O-'),('AB+','AB+'),('AB-','AB-')], blank=True)
    height_cm = models.PositiveIntegerField(blank=True,null=True)
    weight_kg = models.PositiveIntegerField( blank=True,null=True)
    eye_color = models.CharField(max_length=30, blank=True,null=True)
    hair_color = models.CharField(max_length=30, blank=True,null=True)
    skin_tone = models.CharField(max_length=50, blank=True,null=True)
    education_level = models.CharField(max_length=100, blank=True,null=True)
    compensation_packagr=models.PositiveBigIntegerField(blank=True,null=True)
    is_anonymous=models.BooleanField(default=True)
    genetic_screening_cleared=models.BooleanField(default=False)
    screening_expiry_date=models.DateField(null=True,blank=True,help_text="Infections screening usually expire every 6 months.")

    is_active=models.BooleanField(default=True)
    date_assigned=models.DateField(auto_now_add=True)
    def save(self,*args,**kwargs):
        if not self.donor_code:
            last_donor=DonorProfile.objects.all().order_by('id').last()
            if not last_donor:
                self.donor_code="DON001"
            else:
                last_code=last_donor.donor_code
                number_part=re.findall(r'\d+',last_code)

                if number_part:
                    new_number=int(number_part[0])+1
                    self.donor_code = f"DON{new_number:03d}"
                else:
                    self.donor_code="DON001"
        super(DonorProfile, self).save(*args, **kwargs)

    def is_eligible(self):
        from datetime import date
        if not self.genetic_screening_cleared:
            return False
        if self.screening_expiry_date and self.screening_expiry_date<date.today():
            return False
        return True
    
    def __str__(self):
        return f"Donor Code: {self.donor_code}"

