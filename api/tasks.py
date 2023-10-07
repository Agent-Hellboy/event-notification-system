# In your Django app's views.py

from queue import Queue
import threading
import time
import requests

# Define the API endpoints
base_url = "http://127.0.0.1:8000/api/"
get_events_url = f"{base_url}events/"
send_event_emails_url = f"{base_url}send_event_emails/"

# Create a queue to store events for processing
event_queue = Queue()

class Producer(threading.Thread):
    def run(self):
        while True:
            try:
                # Fetch events for today using a GET request
                response = requests.get(get_events_url)
                if response.status_code == 200:
                    events = response.json()
                    for event in events:
                        event_queue.put(event)
                else:
                    print("Failed to fetch events for today.")
                time.sleep(60 * 60)  # Fetch events every hour
            except Exception as e:
                print(f"Error in Producer: {str(e)}")

class Consumer(threading.Thread):
    def run(self):
        while True:
            try:
                # Process events from the queue and send event emails
                if not event_queue.empty():
                    event = event_queue.get()
                    event_type = event["event_type"]
                    payload = {"event_type": event_type}

                    response = requests.post(send_event_emails_url, json=payload)

                    if response.status_code == 201:
                        print(f"Email sent successfully for event type: {event_type}")
                    else:
                        print(f"Failed to send email for event type: {event_type}, Status Code: {response.status_code}")
                time.sleep(60)  # Process events every minute
            except Exception as e:
                print(f"Error in Consumer: {str(e)}")