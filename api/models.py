from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    class Meta:
        app_label = 'api'

class Event(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    event_date = models.DateField()
    processed_today = models.BooleanField(default=False)
    class Meta:
        app_label = 'api'

class EmailTemplate(models.Model):
    event_type = models.CharField(max_length=50)
    template_content = models.TextField()
    class Meta:
        app_label = 'api'

class EmailLog(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=50)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    error_message = models.TextField(null=True, blank=True)
    class Meta:
        app_label = 'api'
