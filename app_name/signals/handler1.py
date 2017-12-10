# Register handlers

from django.dispatch import receiver
from app_name.signals import dummy_signal


@receiver(dummy_signal, sender=None)
def on_dummy_signal(sender, availability_request, **kwargs):
    pass

