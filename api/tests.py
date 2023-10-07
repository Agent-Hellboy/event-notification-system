from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Employee, Event, EmailTemplate, EmailLog
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class YourAppTestCase(TestCase):
    def setUp(self):
        # Create test data for your models
        self.employee = Employee.objects.create(name="Test Employee", email="test@example.com")
        self.event = Event.objects.create(employee=self.employee, event_type="Birthday", event_date="2023-10-10")
        self.email_template = EmailTemplate.objects.create(event_type="Birthday", template_content="Happy Birthday, {{employee_name}}!")

        self.client = APIClient()
        self.superuser = User.objects.create_superuser(
            username="testsuser",
            email="testsuser@example.com",
            password="testspassword"
        )
        self.token = Token.objects.create(user=self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_employee_model(self):
        self.assertEqual(str(self.employee.name), "Test Employee")

    def test_event_model(self):
        self.assertEqual(self.event.event_type, "Birthday")

    def test_email_template_model(self):
        self.assertEqual(self.email_template.event_type, "Birthday")

    def test_api_views(self):
        url = reverse("get_events") 
        data = {"event_type": "Birthday", "event_date": "2023-10-10"}  
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

