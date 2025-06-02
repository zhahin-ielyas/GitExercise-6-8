from django.db.models.signals import post_save
from django.dispatch import receiver
from pantry.models import PantryItem
from .utils import send_expiry_alerts

@receiver(post_save, sender=PantryItem)
def send_alert_on_pantry_update(sender, instance, created, **kwargs):
    user = instance.user
    send_expiry_alerts(user)
