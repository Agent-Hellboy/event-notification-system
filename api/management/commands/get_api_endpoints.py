from django.core.management.base import BaseCommand
from django.urls import get_resolver
from rest_framework.decorators import api_view

class Command(BaseCommand):
    help = 'List all registered API endpoints'

    def handle(self, *args, **options):
        resolver = get_resolver()
        api_endpoints = []

        for url_pattern in resolver.url_patterns:
            if hasattr(url_pattern.callback, 'cls') and issubclass(url_pattern.callback.cls, api_view):
                api_endpoints.append(url_pattern.pattern)

        self.stdout.write("Registered API endpoints:")
        for endpoint in api_endpoints:
            self.stdout.write(f"- {endpoint}")
