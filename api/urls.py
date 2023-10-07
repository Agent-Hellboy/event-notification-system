from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.get_events, name='get_events'),
    path('all_events/', views.get_all_events, name='get_all_events'),
    path('send_event_emails/', views.send_event_emails, name='send_event_emails'),
    path('employee/', views.get_employee, name='get_employee'),
    path('emaillog/', views.get_emaillog, name='get_emaillog'),
    path('emailtemplate/', views.get_emailtemplate, name='get_emailtemplate'),
]