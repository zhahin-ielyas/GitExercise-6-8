"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

 HEAD
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_meal_plan.settings')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
 52899d0 (Updated dashboard.html before merging)

application = get_asgi_application()
