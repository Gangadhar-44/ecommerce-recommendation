"""
WSGI config for ecommerce_recommendation project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_recommendation.settings')

application = get_wsgi_application()
