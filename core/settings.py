"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "0$w&yk9mq#7h$(b$m4-m26!hcyoxaejiq$_sh4u-k==pvs@-74"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG") == 'True'

ALLOWED_HOSTS = [
    "api.learningpost.ng",
    "www.api.learningpost.ng",
    # "app.learningpost.ng",
    # "www.app.learningpost.ng",
    # "portal.admin.learningpost.ng",
    # "www.portal.admin.learningpost.ng",
    # "learningpostchallengesocket.onrender.com",
    "localhost",
    "127.0.0.1",
]

CORS_ALLOWED_ORIGINS = [
    "https://learningpost.ng",
    "https://api.learningpost.ng",
    "https://admin.learningpost.ng",
    "https://pro.learningpost.ng",

    "https://www.learningpost.ng",
    "https://www.api.learningpost.ng",
    "https://www.admin.learningpost.ng",
    "https://www.pro.learningpost.ng",
    
    "wss://learningpostchallengesocket.onrender.com",
    "http://localhost:5000",
    "http://localhost:3000",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'website',
    'admin_app',
    'learningpost_professional',
    'akada',
    'challenge_app',
    'endpoints',
    'smartlink',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'admin_app.context_processors.unread_report_count'
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = (BASE_DIR / 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# if DEBUG:
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
# else:
#     AWS_ACCESS_KEY_ID = config('B2_APPLICATION_KEY_ID')
#     AWS_SECRET_ACCESS_KEY = config('B2_APPLICATION_KEY')
#     AWS_STORAGE_BUCKET_NAME = config('B2_BUCKET_NAME')
#     AWS_S3_REGION_NAME = config('B2_BUCKET_REGION')
#     AWS_S3_ENDPOINT = f's3.{AWS_S3_REGION_NAME}.backblazeb2.com'
#     AWS_S3_ENDPOINT_URL = f'https://{AWS_S3_ENDPOINT}'
#     AWS_DEFAULT_ACL = 'public-read'
#     # Adjust based on your needs

#     DEFAULT_FILE_STORAGE = 'storages.b2.BackblazeB2Storage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'website.user'
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.learningpost.ng'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# CUSTOM CONFIGS
DATA_UPLOAD_MAX_NUMBER_FIELDS = 300000
