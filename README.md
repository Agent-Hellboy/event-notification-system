# Event-Notification-System



## Prerequisites

Before you begin, make sure you have the following prerequisites installed on your system:

- [Python](https://www.python.org/downloads/): You need Python installed to run the application.
- [pip](https://pip.pypa.io/en/stable/installation/): The Python package manager.

## Usage

1. **Clone the Repository**

   Clone this repository to your local machine using Git:

   ```bash
   git clone https://github.com/Agent-Hellboy/event-notification-system.git


2. **Install the requirements**

    ```py 
       cd event-notification-system
       pip install -r requirements.txt

3. **Run db migration commands**
    ```py 
    python3 manage.py makemigrations
    python3 manage.py migrate

3. **Populate db with dummy data**
    ```py 
    python3 manage.py populate_tables

4. ***Run server** 
    ```py 
       python3 manage.py runserver

5. **Test application**

    ```py 
       python3 manage.py test
    