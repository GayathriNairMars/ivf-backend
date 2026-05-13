from django.db import models
from django.conf import settings
import os
from patients.models import PatientProfile

#upload path 
def emr_upload_path(instance,filename):
	patient_id=instance.record.patient.patient_id
	record_type=instance.record.record_type.lower()
	return f"emr/{patient_id}/{record_type}/{filename}"

def medical_history_upload_path(instance,filename):
	return f"emr/{instance.patient.patient_id}/history/{filename}"

#Choices

CYCLE_TYPES=[
    ('IVF','In Vitro Fertilization(IVF) Cycle'),
    ('IUI','IntraUterine Insemination(IUI) Cycle'),
    ('FET','Frozen Embryo Transfer(FET)'),
    ('ICSI','ICSI Cycle'),
    ('OI','Ovulation Induction'),
    ('IVM','In Vitro Maturation'),
    ('EGG_FREEZE','Egg Freezing'),
    ('EMBRYO_FREEZE','Embryo Freezing'),
    ('SPERM_FREEZE','Sperm Freezing'),
    ('PGT','PGT Cycle'),
    ('OTHER','Other'),
]

CYCLE_STATUS = [
	('ONGOING','Ongoing'),
	('COMPLETED','Completed'),
	('CANCELLED','Cancelled'),
	('ON_HOLD','On Hold'),
]

RECORD_TYPE = [
	('CONSULTATION','Consultation'),
	('DIAGNOSIS','Diagnosis'),
	('PRESCRIPTION','Prescription'),
	('LAB_RESULT','Lab Result'),
	('SCAN','Scan / Ultrasound'),
	('PROCEDURE','Procedure Note'),
	('CYCLE','Treatment Cycle'),
  ('NURSING_NOTE',     'Nursing Note'),
  ('PHARMACY_NOTE',    'Pharmacy Note'),
  ('ANDROLOGY_NOTE',   'Andrology Note'),
  ('COUNSELLING_NOTE', 'Counselling Note'),
	('OTHER','Other'),
]

DOCUMENT_TYPES = [
	('PREV_RECORD','Previous Medical Record'),
	('DISCHARGE','Discharge Summary'),
	('PRESCRIPTION','Old Precription'),
	('LAB_REPORT','Old Lab Report'),
	('SCAN','Old Scan'),
	('REFERRAL','Referral Letter'),
	('OTHER','Other'),
]

#ROLES => Allowed record types
ROLE_ALLOWED_RECORD_TYPES = {
    'REC': ['OTHER'],
    'CCO': ['COUNSELLING_NOTE', 'OTHER'],
    'FCO': ['OTHER'],
    'END': ['CONSULTATION', 'DIAGNOSIS', 'PRESCRIPTION', 'SCAN', 'PROCEDURE', 'CYCLE', 'OTHER'],
    'GYN': ['CONSULTATION', 'DIAGNOSIS', 'PRESCRIPTION', 'SCAN', 'PROCEDURE', 'OTHER'],
    'ANE': ['CONSULTATION', 'PROCEDURE', 'OTHER'],
    'EMB': ['PROCEDURE', 'CYCLE', 'LAB_RESULT', 'OTHER'],
    'NUR': ['NURSING_NOTE', 'PRESCRIPTION', 'OTHER'],
    'PHA': ['PHARMACY_NOTE', 'PRESCRIPTION', 'OTHER'],
    'TEC': ['LAB_RESULT', 'OTHER'],
    'AND': ['ANDROLOGY_NOTE', 'LAB_RESULT', 'OTHER'],
    'ADM': [r[0] for r in RECORD_TYPE],
    'HRM': [],
    'PAT': [],
}
 

#EMR record


class EMRRecord(models.Model):
	patient = models.ForeignKey(PatientProfile,on_delete=models.CASCADE,related_name='emr_records',)
	created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='emr_entries')
	record_type=models.CharField(max_length=20, choices=RECORD_TYPE,default='CONSULTATION')
	title=models.CharField(max_length=200)
	date=models.DateField()
	notes=models.TextField(blank=True)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)

	class Meta:
		ordering=['-date','-created_at']
	
	def __str__(self):
		return f"{self.patient.patient_id} - {self.record_type} - {self.date}"
	
	@classmethod
	def allowed_types_for_Role(cls,role):
		return ROLE_ALLOWED_RECORD_TYPES.get(role,[])
	
#Sub-sections

class ConsultationNote(models.Model):
	#"""Roles: END,GYN,ANE"""
	record = models.OneToOneField(EMRRecord,on_delete=models.CASCADE,related_name='consultation')
	chief_complaint=models.TextField(blank=True)
	history=models.TextField(blank=True)
	examination=models.TextField(blank=True)
	assessment=models.TextField(blank=True)
	plan=models.TextField(blank=True)

	def __str__(self):
		return f"Consultation - {self.record}"

class Diagnosis(models.Model):
	#ROLES: END, GYN
	record=models.ForeignKey(EMRRecord,on_delete=models.CASCADE,related_name='diagnosis')
	icd_code=models.CharField(max_length=20,blank=True)
	description=models.TextField()
	is_primary=models.BooleanField(default=False)

	def __str__(self):
		return f"{self.icd_code} - {self.description[:50]}"
	
class Prescription(models.Model):
	#ROLES: END,GYN,NUR,PHA
	record=models.ForeignKey(EMRRecord,on_delete=models.CASCADE,related_name='prescriptions')
	medication_name=models.CharField(max_length=200)
	dosage=models.CharField(max_length=100,blank=True)
	frequency=models.CharField(max_length=100,blank=True)
	duration=models.CharField(max_length=100,blank=True)
	route=models.CharField(max_length=50,blank=True,help_text="e.g. Oral, IM, IV")
	instructions=models.TextField(blank=True)

	def __str__(self):
		return f"{self.medication_name} - {self.dosage}"

class LabResult(models.Model):
	#ROLES: TEC,AND,EMB,GYN
	record = models.ForeignKey(EMRRecord,on_delete=models.CASCADE,related_name='lab_results')
	test_name=models.CharField(max_length=200)
	result_value=models.CharField(max_length=100,blank=True)
	unit=models.CharField(max_length=50,blank=True)
	reference_range=models.CharField(max_length=100,blank=True)
	is_abnormal=models.BooleanField(default=False)
	notes=models.TextField(blank=True)

	#file uploads
	report_file=models.FileField(upload_to=emr_upload_path,null=True,blank=True,help_text="Upload lab report pdf")

	report_image=models.ImageField(upload_to=emr_upload_path,null=True,blank=True,help_text="Upload  lab report image (JPG,PNG)")

	def __str__(self):
		return f"{self.test_name}: {self.result_value} {self.unit}"

class ScanReport(models.Model):
	#ROLES: END,GYN
	record = models.ForeignKey(EMRRecord,on_delete=models.CASCADE,related_name='scans')
	scan_type=models.CharField(max_length=100,blank=True,help_text="e.g. TVS USG, Abdominal USG")
	findings=models.TextField(blank=True)
	follicle_count=models.PositiveIntegerField(null=True,blank=True)
	endometrium=models.CharField(max_length=100,blank=True,help_text="e.g. 9mm trilaminar")
	impression=models.TextField(blank=True)

	#file upload
	image=models.ImageField(upload_to=emr_upload_path,null=True,blank=True,help_text="Upload scan image (JPG,PNG)")

	report_file=models.FileField(upload_to=emr_upload_path,null=True,blank=True,help_text="Upload scan report PDF")

	def __str__(self):
		return f"{self.scan_type} - {self.record.date}"

class ProcedureNote(models.Model):
	# ROLES: END,GYN,ANE,EMB
	record=models.ForeignKey(EMRRecord,on_delete=models.CASCADE,related_name='procedures')
	procedure_name=models.CharField(max_length=200,help_text="e.g. OPU, Emmbryo Transfer, ICSI")
	performed_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='procedures_performed')

	details=models.TextField(blank=True)
	outcome=models.TextField(blank=True)
	complications=models.TextField(blank=True)

	def __str__(self):
		return f"{self.procedure_name} - {self.record.date}"

class TreatmentCycle(models.Model):
	# ROLES: END,EMB
	record=models.OneToOneField(EMRRecord,on_delete=models.CASCADE,related_name='cycle')
	cycle_type=models.CharField(max_length=20,choices=CYCLE_TYPES)
	cycle_number=models.PositiveIntegerField(default=1)
	start_date=models.DateField(null=True,blank=True)
	end_date=models.DateField(null=True,blank=True)
	status=models.CharField(max_length=20,choices=CYCLE_STATUS,default='ONGOING')

	#IVF Specific
	eggs_retrieved=models.PositiveIntegerField(null=True,blank=True)
	eggs_fertilized=models.PositiveIntegerField(null=True,blank=True)
	embryos_formed=models.PositiveIntegerField(null=True,blank=True)
	embryos_transfered=models.PositiveIntegerField(null=True,blank=True)
	embryos_frozen=models.PositiveIntegerField(null=True,blank=True)

	outcome=models.TextField(blank=True)
	notes=models.TextField(blank=True)

	def __str__(self):
		return f"Cycle {self.cycle_number} - {self.cycle_type} - {self.status}"
	
class NursingNote(models.Model):
	# ROLES: NUR
	record = models.OneToOneField(EMRRecord,on_delete=models.CASCADE,related_name='nursing_note')
	vital_bp=models.CharField(max_length=20, blank=True, help_text="e.g. 120/80 mmHg")
	vital_pulse=models.CharField(max_length=20,blank=True,help_text="e.g. 72bpm")
	vital_temp=models.CharField(max_length=20,blank=True, help_text="e.g. 98.6 F")
	vital_spo2=models.CharField(max_length=20,blank=True,help_text="e.g. 99%")
	vital_weight=models.CharField(max_length=20,blank=True,help_text="e.g. 62kg")
	observations=models.TextField(blank=True)
	medications_given=models.TextField(blank=True, help_text="Medications administered during shift")
	instructions_given=models.TextField(blank=True)

	def __str__(self):
		return f"Nursing Note - {self.record}"

class PharmacyNote(models.Model):
	#ROLES: PHA
	record=models.OneToOneField(EMRRecord,on_delete=models.CASCADE,related_name='pharmacy_note')
	dispensed_items=models.TextField(blank=True,help_text="List of medications dispensed")
	batch_numbers=models.TextField(blank=True)
	dispensing_notes=models.TextField(blank=True)
	counselling_given=models.TextField(blank=True,help_text="Patient counselling notes at dispensing")

	def __str__(self):
		return f"Pharmacy Note - {self.record}"
	
class AndrologyNote(models.Model):
	# ROLES: AND
	record=models.OneToOneField(EMRRecord,on_delete=models.CASCADE,related_name='andrology_note')
	sample_type=models.CharField(max_length=100,blank=True,help_text="e.g. Semen, Biopsy")
	volume_ml=models.DecimalField(max_digits=5,decimal_places=2,null=True, blank=True)
	concentration= models.CharField(max_length=50, blank=True, help_text="e.g. 15 million/mL")
	motility_percent=models.DecimalField(max_digits=5,decimal_places=2,null=True, blank=True)
	morphology_percent=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
	dna_fragmentation=models.DecimalField(max_digits=5,decimal_places=2, null=True, blank=True)
	who_criteria=models.CharField(max_length=20, blank=True, help_text="e.g. WHO 2021")
	impression=models.TextField(blank=True)
	notes=models.TextField(blank=True)
	report_file=models.FileField(upload_to=emr_upload_path, null=True, blank=True, help_text="Upload andrologyy report PDF")
	report_image=models.ImageField(upload_to=emr_upload_path, null=True, blank=True, help_text="Upload andrology report PDF")
	def __str__(self):
		return f"Andrology Note - {self.record}"
	
class CounsellingNote(models.Model):
	# ROLES: CCO
	record=models.OneToOneField(EMRRecord,on_delete=models.CASCADE,related_name='counselling_note')
	session_type=models.CharField(max_length=100, blank=True, help_text="e.g. Pre-IVF, Emotional Support, Outcome")
	concerns_raised=models.TextField(blank=True)
	advice_given=models.TextField(blank=True)
	follow_up_required=models.BooleanField(default=False)
	follow_up_date=models.DateField(null=True, blank=True)
	notes=models.TextField(blank=True)

	def __str__(self):
		return f"Counselling Note - {self.record}"


#Medical history documents
class MedicalHistoryDocument(models.Model):
	patient=models.ForeignKey(PatientProfile,on_delete=models.CASCADE,related_name='history_documents',)
	uploaded_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True, related_name='uploaded_documents')
	document_type=models.CharField(max_length=20,choices=DOCUMENT_TYPES,default='PREV_RECORD')
	title=models.CharField(max_length=200)
	file=models.FileField(upload_to=medical_history_upload_path)
	notes=models.TextField(blank=True)
	document_date=models.DateField(null=True,blank=True,help_text="Date of the original document")
	uploaded_at=models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering=['-uploaded_at']
	
	def __str__(self):
		return f"{self.patient.patient_id} - {self.document_type} - {self.title}"

