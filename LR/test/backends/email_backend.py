# your_app/backends/email_backend.py
from django.core.mail.backends.base import BaseEmailBackend

class EmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        # Your email sending logic here
        pass
