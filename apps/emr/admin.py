from django.contrib import admin

from .models import (EMRRecord,ConsultationNote,Diagnosis,Prescription,LabResult,ScanReport,ProcedureNote,TreatmentCycle,NursingNote,PharmacyNote,AndrologyNote,CounsellingNote,MedicalHistoryDocument,)

class ConsultationNoteInline(admin.StackedInline):
	model=ConsultationNote
	extra=0

class DiagnosisInline(admin.TabularInline):
	model=Diagnosis
	extra=0

class PrescriptionInline(admin.TabularInline):
	model=Prescription
	extra=0

class LabResultInline(admin.TabularInline):
	model=LabResult
	extra=0

class ScanReportInline(admin.TabularInline):
	model=ScanReport
	extra=0

class ProcedureNoteInline(admin.TabularInline):
	model=ProcedureNote
	extra=0

class TreatmentCycleInline(admin.StackedInline):
	model=TreatmentCycle
	extra=0

class NursingNoteInline(admin.StackedInline):
	model=NursingNote
	extra=0

class PharmacyNoteInline(admin.StackedInline):
	model=PharmacyNote
	extra=0

class AndrologyNoteInline(admin.StackedInline):
	model=AndrologyNote
	extra=0

class CounsellingNoteInline(admin.StackedInline):
	model=CounsellingNote
	extra=0

@admin.register(EMRRecord)
class EMRRecordAdmin(admin.ModelAdmin):
	list_display=['patient','record_type','title','date','created_by','created_at']
	list_filter=['record_type','date','created_by__role']
	search_fields=['patient__patient_id','title','created_by__full_name']
	inlines=[ConsultationNoteInline,DiagnosisInline,PrescriptionInline,LabResultInline,ScanReportInline,ProcedureNoteInline,TreatmentCycleInline,NursingNoteInline,PharmacyNoteInline,AndrologyNoteInline,CounsellingNoteInline,]

@admin.register(MedicalHistoryDocument)
class MedicalHistoryDocumentAdmin(admin.ModelAdmin):
	list_display=['patient','document_type','title','document_date','uploaded_by','uploaded_at']
	list_filter=['document_type']
	search_fields=['patient__patient_id','title','uploaded_by__full_name']
