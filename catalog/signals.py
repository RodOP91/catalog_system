from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

from anymail.message import AnymailMessage

from .models import Product

User = get_user_model()

@receiver(post_save, sender=Product)
def send_product_notification(sender, instance, created, **kwargs):
    if created:
        # New product creation
        subject = '¡Nuevo producto!'
        body = 'Un nuevo producto ha sido creado.'
    else:
        # Product update
        subject = 'Modificación de Producto'
        body = 'Un producto ha sido modificado.'
    admin_users = User.objects.filter(is_admin=True).values_list('email', flat=True)
    email = AnymailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=admin_users,
    )
    email.send()

@receiver(pre_delete, sender=Product)
def send_product_deletion_notification(sender, instance, **kwargs):
    subject = 'Product Deletion Notification'
    body = 'A product has been deleted.'

    admin_users = User.objects.filter(is_admin=True).values_list('email', flat=True)
    email = AnymailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=admin_users,
    )
    email.send()

@receiver(post_save, sender=User)
def send_user_notification(sender, instance, created, **kwargs):
    if created:
        # New user creation
        subject = 'New User Notification'
        body = 'A new user has been created.'
    else:
        # User update
        subject = 'User Update Notification'
        body = 'A user has been updated.'

    admin_users = User.objects.filter(is_admin=True).values_list('email', flat=True)
    email = AnymailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=admin_users,
    )
    email.send()

@receiver(pre_delete, sender=User)
def send_user_deletion_notification(sender, instance, **kwargs):
    subject = 'User Deletion Notification'
    body = 'A user has been deleted.'

    admin_users = User.objects.filter(is_admin=True).values_list('email', flat=True)
    email = AnymailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=admin_users,
    )
    email.send()