from datetime import datetime
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Event, EmailTemplate, EmailLog, Employee
from .serializers import EventSerializer, EmailLogSerializer,EmployeeSerializer,EmailTemplateSerializer
from .utils import send_email, populate_email_template

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

@api_view(['GET','POST'])
@permission_classes([IsAdminUser])
def get_events(request):
    if request.method == 'GET':
        # Retrieve events based on the current date
        current_date = datetime.now().date()
        events = Event.objects.filter(event_date=current_date)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def get_employee(request):
    if request.method == 'GET':
        # Retrieve all employees
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new employee
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_emaillog(request):
    email_log = EmailLog.objects.all()
    serializer = EmailLogSerializer(email_log, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_emailtemplate(request):
    email_log = EmailTemplate.objects.all()
    serializer = EmailTemplateSerializer(email_log, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_events(request):
    # Retrieve all events
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_event_emails(request):
    event_type = request.data.get('event_type')
    current_date = datetime.now().date()
    
    try:
        # Retrieve event details and email template
        event = get_object_or_404(Event, event_type=event_type, event_date=current_date)
        email_template = get_object_or_404(EmailTemplate, event_type=event_type)
        
        # Check if the event has already been processed today
        if event.processed_today:
            return Response({'message': 'Event has already been processed today'}, status=status.HTTP_200_OK)
        
        # Create and send personalized email
        email_content = populate_email_template(email_template, event.employee)
        send_email(event.employee.email, email_content)
        
        # Log email sending status
        email_log = EmailLog(employee=event.employee, event_type=event.event_type, status='Sent')
        email_log.save()
        
        # Mark the event as processed for today
        event.processed_today = True
        event.save()
        
        return Response({'message': 'Email sent successfully'}, status=status.HTTP_201_CREATED)
    
    except Event.DoesNotExist:
        return Response({'message': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
    
    except EmailTemplate.DoesNotExist:
        return Response({'message': 'Email template not found'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        # Log email sending error
        email_log = EmailLog(event_type=event_type, status='Error', error_message=str(e))
        email_log.save()
        return Response({'message': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)