"""
WSGI config for EasShip project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import sys

sys.path.append('/home/ubuntu/myproject/worka/workadaptar')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EasShip.settings')

application = get_wsgi_application()
