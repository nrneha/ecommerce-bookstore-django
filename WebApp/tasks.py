from celery import shared_task
from django.core.mail import EmailMessage


@shared_task()
def send_email(subject, body, email):        
    email = EmailMessage(subject, body, to=[email])
    email.content_subtype = "html"
    email.send()
    return "Email sent successfully"