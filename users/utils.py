from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import date, timedelta
from pantry.models import PantryItem

def send_expiry_alerts(user):
    today = date.today()
    soon_threshold = today + timedelta(days=3)

    expired_items = PantryItem.objects.filter(user=user, expiry_date__lt=today)
    expiring_soon_items = PantryItem.objects.filter(user=user, expiry_date__gte=today, expiry_date__lte=soon_threshold)

    if not expired_items.exists() and not expiring_soon_items.exists():
        return  # Nothing to alert

    html_message = render_to_string('email/expiry_alert.html', {
        'user': user,
        'expired_items': expired_items,
        'expiring_soon_items': expiring_soon_items,
    })

    plain_message = strip_tags(html_message)
    subject = 'Pantry Expiry Alert'
    from_email = None  # Uses DEFAULT_FROM_EMAIL setting

    send_mail(subject, plain_message, from_email, [user.email], html_message=html_message)
