"""
WSGI config for django_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application 

# Calculate base directory (three levels up)
BASE_DIR = Path(__file__).resolve().parent.parent
#sys.path.insert(0, str(BASE_DIR))

settings_module = 'django_app.deployment' if 'RENDER_EXTERNAL_HOSTNAME' in os.environ else 'django_app.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.django_app.settings')



application = get_wsgi_application()
