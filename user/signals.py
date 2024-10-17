from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(user_logged_in)
def send_login_notification(sender, request, user, **kwargs):
    subject = 'Login Notification'
    message = f'{user.username} logged in successfully.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)

@receiver(user_logged_out)
def send_logout_notification(sender, request, user, **kwargs):
    subject = 'Logout Notification'
    message = f'{user.username} logged out successfully.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)