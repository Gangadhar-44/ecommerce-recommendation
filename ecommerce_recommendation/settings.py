"""
Django settings for ecommerce_recommendation project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-recommendation-engine-2024-secure-key'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'recommendations',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'recommendations.middleware.UserBehaviorMiddleware',
]

ROOT_URLCONF = 'ecommerce_recommendation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_recommendation.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Use SQLite for demo (no MySQL setup needed)
DATABASES['default'] = DATABASES['sqlite']

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'recommendations', 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Recommendation Engine Settings
RECOMMENDATION_SETTINGS = {
    'COLLABORATIVE_FILTERING': {
        'K_NEIGHBORS': 5,
        'MIN_RATINGS': 2,
        'SIMILARITY_THRESHOLD': 0.3,
    },
    'CONTENT_BASED': {
        'WEIGHT_CATEGORY': 0.4,
        'WEIGHT_PRICE': 0.2,
        'WEIGHT_BRAND': 0.2,
        'WEIGHT_TAGS': 0.2,
    },
    'HYBRID': {
        'CF_WEIGHT': 0.6,
        'CB_WEIGHT': 0.4,
    }
}

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
