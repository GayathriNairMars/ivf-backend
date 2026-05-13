from django.shortcuts import render
from rest_framework import viewsets
from .serializer import PatientUserCreateSerializer
from accounts.models import User,ReceptionistProfile
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from .permissions import AppointmentPermissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash

class ReceptionistView(viewsets.ModelViewSet):
    queryset=User.objects.filter(role__in=['PAT','DON'])
    serializer_class=PatientUserCreateSerializer
    permission_classes=[AppointmentPermissions]
    parser_classes=[FormParser,MultiPartParser]
    renderer_classes=[TemplateHTMLRenderer,JSONRenderer]

    @action(detail=False,methods=['get'],url_path='patient')
    def onboard(self,request):
        return Response({},template_name='receptionist/create_patient.html')
    def list(self,request,*args,**kwargs):
        queryset=self.get_queryset()

        patients=queryset.filter(role='PAT')
        donors=queryset.filter(role='DON')
        
        if request.accepted_renderer.format=='html':
            return Response({
                'patients':patients,
                'donors':donors
                },
                template_name='receptionist/patient-donor_list.html'
                )
        return super().list(request,*args,**kwargs)
    
    
    def create(self,request,*args,**kwargs):
        response=super().create(request,*args,**kwargs)
        if request.accepted_renderer.format=='html':
            return redirect('appointments:receptionist_view-list')
        return response
    
    @action(detail=False,methods=['get'],url_path='dashboard')
    def dashboard(self,request):
        patients_count=User.objects.filter(role__in=['PAT']).count()
        donors_count=User.objects.filter(role__in=['DON']).count()
        if request.accepted_renderer.format=='html':
            return Response({'patients_count':patients_count,'donor_count':donors_count},template_name='receptionist/reg_dashboard.html')
        return Response({'patients_count':patients_count,'donors_count':donors_count})
    
    @action(detail=False,methods=['get','post'],url_path='my_profile')
    def my_profile(self,request):
        user=request.user
        is_editing=request.GET.get('edit') == 'true'
        change_password=request.GET.get('password') == 'true'
        if request.method=='GET':
            context={
                'user':user,
                'is_editing':is_editing,
                'change_password':change_password
            }
            if user.role=='REC':
                profile,_=ReceptionistProfile.objects.get_or_create(user=user)
                context['profile']=user.receptionist_profile
            return Response(context,template_name='receptionist/my_profile.html')
        
        if request.method=='POST':
            if 'new_password' in request.data:
                old_pass=request.data.get('old_password')
                new_pass=request.data.get('new_password')
                if user.check_password(old_pass):
                    user.set_password(new_pass)
                    user.save()
                    update_session_auth_hash(request,user)
                    return redirect('appointments:receptionist_view-my-profile')
                else:
                    return Response({'user':user,'error':'Incorrect Old Password'},template_name='receptionist/my_profile.html')
            if user.role =='REC':
                profile=user.receptionist_profile
                profile.desk_location=request.data.get('desk_location','')
                profile.contact_number=request.data.get('contact_number','')
                profile.save()
                profile.refresh_from_db()
            return redirect('appointments:receptionist_view-my-profile')
    