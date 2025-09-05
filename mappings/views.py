from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer, PatientDoctorMappingCreateSerializer
from patients.models import Patient

class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctorMapping.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PatientDoctorMappingCreateSerializer
        return PatientDoctorMappingSerializer
    
    def create(self, request):
        """Assign a doctor to a patient"""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Verify patient belongs to the requesting user
                patient = serializer.validated_data['patient']
                if patient.created_by != request.user:
                    return Response({
                        'error': 'Permission denied',
                        'details': 'You can only assign doctors to your own patients'
                    }, status=status.HTTP_403_FORBIDDEN)
                
                mapping = serializer.save()
                return Response({
                    'message': 'Doctor assigned to patient successfully',
                    'mapping': PatientDoctorMappingSerializer(mapping).data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'error': 'Assignment failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        """Get all patient-doctor mappings"""
        try:
            # Filter to show only mappings for patients created by the user
            user_patients = Patient.objects.filter(created_by=request.user)
            queryset = self.get_queryset().filter(patient__in=user_patients)
            serializer = self.get_serializer(queryset, many=True)
            
            return Response({
                'count': queryset.count(),
                'mappings': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'], url_path='patient/(?P<patient_id>[^/.]+)')
    def get_patient_doctors(self, request, patient_id=None):
        """Get all doctors assigned to a specific patient"""
        try:
            # Verify patient exists and belongs to the user
            patient = Patient.objects.filter(id=patient_id, created_by=request.user).first()
            if not patient:
                return Response({
                    'error': 'Patient not found or access denied'
                }, status=status.HTTP_404_NOT_FOUND)
            
            mappings = self.get_queryset().filter(patient_id=patient_id)
            serializer = self.get_serializer(mappings, many=True)
            
            return Response({
                'patient_name': patient.name,
                'doctors_count': mappings.count(),
                'mappings': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None):
        """Remove a doctor from a patient (soft delete)"""
        try:
            mapping = self.get_queryset().filter(pk=pk).first()
            if not mapping:
                return Response({
                    'error': 'Mapping not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Verify patient belongs to the requesting user
            if mapping.patient.created_by != request.user:
                return Response({
                    'error': 'Permission denied',
                    'details': 'You can only modify mappings for your own patients'
                }, status=status.HTTP_403_FORBIDDEN)
            
            mapping.is_active = False
            mapping.save()
            
            return Response({
                'message': 'Doctor removed from patient successfully'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)