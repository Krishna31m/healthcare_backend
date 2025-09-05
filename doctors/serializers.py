from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_email(self, value):
        doctor_id = self.instance.id if self.instance else None
        if Doctor.objects.filter(email=value).exclude(id=doctor_id).exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        return value

    def validate_license_number(self, value):
        doctor_id = self.instance.id if self.instance else None
        if Doctor.objects.filter(license_number=value).exclude(id=doctor_id).exists():
            raise serializers.ValidationError("A doctor with this license number already exists.")
        return value

    def validate_years_of_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("Years of experience cannot be negative.")
        if value > 60:
            raise serializers.ValidationError("Years of experience seems unrealistic.")
        return value