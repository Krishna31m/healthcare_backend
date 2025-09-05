from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Doctor
from .serializers import DoctorSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        """Create a new doctor"""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                doctor = serializer.save()
                return Response({
                    'message': 'Doctor created successfully',
                    'doctor': serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'error': 'Doctor creation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        """Get all doctors"""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            
            return Response({
                'count': queryset.count(),
                'doctors': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def retrieve(self, request, pk=None):
        """Get details of a specific doctor"""
        try:
            doctor = self.get_queryset().filter(pk=pk).first()
            if not doctor:
                return Response({
                    'error': 'Doctor not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.get_serializer(doctor)
            return Response({
                'doctor': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk=None):
        """Update doctor details"""
        try:
            doctor = self.get_queryset().filter(pk=pk).first()
            if not doctor:
                return Response({
                    'error': 'Doctor not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.get_serializer(doctor, data=request.data, partial=True)
            if serializer.is_valid():
                doctor = serializer.save()
                return Response({
                    'message': 'Doctor updated successfully',
                    'doctor': serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                'error': 'Doctor update failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None):
        """Delete a doctor record"""
        try:
            doctor = self.get_queryset().filter(pk=pk).first()
            if not doctor:
                return Response({
                    'error': 'Doctor not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            doctor.delete()
            return Response({
                'message': 'Doctor deleted successfully'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)