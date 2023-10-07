from django.core.management.base import BaseCommand
from api.models import Employee, Event, EmailTemplate, EmailLog

class Command(BaseCommand):
    help = 'Populate tables with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Populating tables with initial data...')
        
        # Create employees
        employee1 = Employee.objects.create(name='John Doe', email='john@example.com')
        employee2 = Employee.objects.create(name='Jane Smith', email='jane@example.com')

        # Create events
        event1 = Event.objects.create(employee=employee1, event_type='Birthday', event_date='2023-10-10')
        event2 = Event.objects.create(employee=employee2, event_type='Work Anniversary', event_date='2023-11-15')

        # Create email templates
        email_template1 = EmailTemplate.objects.create(event_type='Birthday', template_content='Happy Birthday, {{employee_name}}!')
        email_template2 = EmailTemplate.objects.create(event_type='Work Anniversary', template_content='Congratulations on your work anniversary, {{employee_name}}!')

        self.stdout.write(self.style.SUCCESS('Tables populated successfully.'))
