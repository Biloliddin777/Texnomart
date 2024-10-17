from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from rest_framework.authtoken.admin import User
from .models import Category, Product
import json
import os
from django.conf import settings


@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    if created:
        subject = 'Product Created'
        message = f'Dear user, {instance.name} was created.'
        from_email = 'biloliddin14042009@gmail.com'
        recipient_list = [user.email for user in User.objects.all()]

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )


post_save.connect(product_post_save, sender=Product)


@receiver(pre_delete, sender=Product)
def save_product_to_json_before_delete(sender, instance, **kwargs):
    file_path = os.path.join(settings.BASE_DIR, 'deleted_data.json')

    data = {
        "model": instance.__class__.__name__,
        "data": {
            "id": instance.id,
            "name": getattr(instance, 'name', None),
            "title": getattr(instance, 'title', None),
            "created_at": instance.created_at.strftime('%Y-%m-%d %H:%M:%S') if instance.created_at else None,
            "updated_at": instance.updated_at.strftime('%Y-%m-%d %H:%M:%S') if instance.updated_at else None,
        }
    }

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(data)

    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)


@receiver(post_save, sender=Category)
def category_post_save(sender, instance, created, **kwargs):
    if created:
        subject = 'Category Created'
        message = f'Dear user, {instance.title} was created.'
        from_email = 'biloliddin14042009@gmail.com'
        recipient_list = [user.email for user in User.objects.all()]

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )


@receiver(pre_delete, sender=Category)
def save_category_to_json_before_delete(sender, instance, **kwargs):
    file_path = os.path.join(settings.BASE_DIR, 'deleted_data.json')

    data = {
        "model": instance.__class__.__name__,
        "data": {
            "id": instance.id,
            "title": getattr(instance, 'title', None),
            "created_at": instance.created_at.strftime('%Y-%m-%d %H:%M:%S') if instance.created_at else None,
            "updated_at": instance.updated_at.strftime('%Y-%m-%d %H:%M:%S') if instance.updated_at else None,
        }
    }

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(data)

    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)
