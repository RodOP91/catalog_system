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
        subject = 'New Product Notification'
        body = 'A new product has been created.'
    else:
        # Product update
        subject = 'Product Update Notification'
        body = 'A product has been updated.'

    email = AnymailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['rodrigo.op1791@gmail.com'],
    )
    email.send()

@receiver(pre_delete, sender=Product)
def send_product_deletion_notification(sender, instance, **kwargs):
    subject = 'Product Deletion Notification'
    body = 'A product has been deleted.'

    email = AnymailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['rodrigo.op1791@gmail.com'],
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

    email = AnymailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['rodrigo.op1791@gmail.com'],
    )
    email.send()

@receiver(pre_delete, sender=User)
def send_user_deletion_notification(sender, instance, **kwargs):
    subject = 'User Deletion Notification'
    body = 'A user has been deleted.'

    email = AnymailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['rodrigo.op1791@gmail.com'],
    )
    email.send()



"""from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

from anymail.message import AnymailMessage



User = get_user_model()

@receiver(post_save, sender=User)
def send_notification_on_update(sender, instance, **kwargs):
    if instance.is_admin:
        email = AnymailMessage(
            subject='Modificación de producto',
            body='Un producto ha sido modificado por un admin.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['rodrigo.op1791@gmail.com'],  
        )
        email.send()

@receiver(pre_delete, sender=User)
def send_notification_on_delete(sender, instance, **kwargs):
    if instance.is_admin:
        email = AnymailMessage(
            subject='Notificación Borrado',
            body='A product has been deleted by another admin.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['rodrigo.op1791@gmail.com'],
        )
        email.send()
"""