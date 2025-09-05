from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_details = PatientSerializer(source='patient', read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = '__all__'
        read_only_fields = ('id', 'assigned_at')

    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        
        # Check if mapping already exists
        if self.instance is None:  # Creating new mapping
            if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor, is_active=True).exists():
                raise serializers.ValidationError("This patient is already assigned to this doctor.")
        
        return attrs

class PatientDoctorMappingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ('patient', 'doctor', 'notes')

    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor, is_active=True).exists():
            raise serializers.ValidationError("This patient is already assigned to this doctor.")
        
        return attrs