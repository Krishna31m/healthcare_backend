from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

    def validate_email(self, value):
        patient_id = self.instance.id if self.instance else None
        if Patient.objects.filter(email=value).exclude(id=patient_id).exists():
            raise serializers.ValidationError("A patient with this email already exists.")
        return value

class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('name', 'email', 'phone', 'date_of_birth', 'gender', 'address', 'medical_history')

    def validate_email(self, value):
        if Patient.objects.filter(email=value).exists():
            raise serializers.ValidationError("A patient with this email already exists.")
        return value