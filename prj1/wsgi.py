"""
WSGI config for prj1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prj1.settings')
application = get_wsgi_application()
application = WhiteNoise(application, root=settings.STATIC_ROOT)
application.add_files(os.path.join(settings.STATIC_ROOT, "js"), prefix="static/js/")
#application.mime_types.add_type("application/javascript", ".js")