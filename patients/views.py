from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Patient
from .serializers import PatientSerializer, PatientCreateSerializer

class PatientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PatientCreateSerializer
        return PatientSerializer
    
    def create(self, request):
        """Create a new patient"""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                patient = serializer.save(created_by=request.user)
                return Response({
                    'message': 'Patient created successfully',
                    'patient': PatientSerializer(patient).data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'error': 'Patient creation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        """Get all patients created by the authenticated user"""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            
            return Response({
                'count': queryset.count(),
                'patients': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def retrieve(self, request, pk=None):
        """Get details of a specific patient"""
        try:
            patient = self.get_queryset().filter(pk=pk).first()
            if not patient:
                return Response({
                    'error': 'Patient not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.get_serializer(patient)
            return Response({
                'patient': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk=None):
        """Update patient details"""
        try:
            patient = self.get_queryset().filter(pk=pk).first()
            if not patient:
                return Response({
                    'error': 'Patient not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.get_serializer(patient, data=request.data, partial=True)
            if serializer.is_valid():
                patient = serializer.save()
                return Response({
                    'message': 'Patient updated successfully',
                    'patient': PatientSerializer(patient).data
                }, status=status.HTTP_200_OK)
            
            return Response({
                'error': 'Patient update failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None):
        """Delete a patient record"""
        try:
            patient = self.get_queryset().filter(pk=pk).first()
            if not patient:
                return Response({
                    'error': 'Patient not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            patient.delete()
            return Response({
                'message': 'Patient deleted successfully'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)