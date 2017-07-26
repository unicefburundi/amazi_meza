"""
Django settings for amazi_meza project.

Generated by 'django-admin startproject' using Django 1.9.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PROJECT_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'amazi_meza_app',
    'public_administration_structure_app',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'amazi_meza.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'amazi_meza.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Bujumbura'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(PROJECT_PATH,  'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_PATH,  'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)

LOGIN_REDIRECT_URL = 'home'


KNOWN_PREFIXES = {
    'RLR': 'COMMUNE_LEVEL_SELF_REGISTRATION',
    'RLRM': 'COMMUNE_LEVEL_SELF_REGISTRATION_M',
    'RL': 'LOCAL_SELF_REGISTRATION',
    'RLC': 'RECORD_NETWORK',
    'RP': 'REPORT_PROBLEM',
    'RPC': 'REPORT_BENEFICIARIES_BASE',
    'RWP': 'REPORT_WATER_SOURCES_POINTS',
    'RWA': 'REPORT_ADDITIONAL_WATER_SOURCES_POINTS',
    'RWF': 'REPORT_FUNCTIONAL_WATER_SOURCES_POINTS',
    'RBB': 'REPORT_ANNUAL_BUDGET',
    'RBE': 'REPORT_EXPECTED_EXPENDITURE',
    'RCI': 'REPORT_INCOME',
    'RIE': 'REPORT_EXPENDITURE',
}


EXPECTED_NUMBER_OF_VALUES = {
    'COMMUNE_LEVEL_SELF_REGISTRATION': 3,
    'COMMUNE_LEVEL_SELF_REGISTRATION_M': 3,
    'LOCAL_SELF_REGISTRATION': 7,
    'RECORD_NETWORK': 2,
    'REPORT_PROBLEM': 6,
    'REPORT_BENEFICIARIES_BASE': 6,
    'REPORT_WATER_SOURCES_POINTS': 7,
    'REPORT_ADDITIONAL_WATER_SOURCES_POINTS': 7,
    'REPORT_FUNCTIONAL_WATER_SOURCES_POINTS': 7,
    'REPORT_ANNUAL_BUDGET': 3,
    'REPORT_EXPECTED_EXPENDITURE': 3,
    'REPORT_INCOME': 4,
    'REPORT_EXPENDITURE': 7,
}



try:
    from localsettings import *
except ImportError:
    pass