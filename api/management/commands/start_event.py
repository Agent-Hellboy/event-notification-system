from django.core.management.base import BaseCommand
from api.tasks import Producer, Consumer

class Command(BaseCommand):
    help = 'Start the event processor'

    def handle(self, *args, **options):
        # Start the producer and consumer tasks
        producer = Producer()
        consumer = Consumer()
        producer.start()
        consumer.start()

        # Wait for the tasks to finish
        producer.join()
        consumer.join()

        self.stdout.write(self.style.SUCCESS('Event processor has finished.'))
