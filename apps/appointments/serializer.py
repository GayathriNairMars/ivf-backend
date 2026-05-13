from rest_framework import serializers
from patients.models import PatientProfile
from donor.models import DonorProfile
from accounts.models import User
class PatientUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= ['id','email','full_name','role','password']
        extra_kwargs={'password':{'write_only':True}}
        
    def validate_role(self, value):
        if value not in ["PAT"]:
            raise serializers.ValidationError(
                "Receptionist can only create Patient or Donor accounts."
            )
        return value
    
    def create(self,validated_data):
        password=validated_data.pop('password')
        user=User.objects.create_user(password=password,**validated_data)

        if user.role=='PAT':
            PatientProfile.objects.create(user=user)
        
        return user
