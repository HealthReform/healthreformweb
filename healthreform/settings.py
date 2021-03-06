"""
Django settings for healthreform project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'px0#7w61zx7s(+spj@*s()==%-4c(3i^&)c)z#0!(57dj996@t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'healthreform.urls'

WSGI_APPLICATION = 'healthreform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'Data_2013',
        'USER': 'tdesai',
        'PASSWORD': '#ToBollywood',
        'HOST': 'fordemo.c91e6955bgwn.us-west-2.rds.amazonaws.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306'
    },
    '2012': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'Data_2012',
        'USER': 'tdesai',
        'PASSWORD': '#ToBollywood',
        'HOST': 'fordemo.c91e6955bgwn.us-west-2.rds.amazonaws.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306'

    },
    '2011': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'Data_2011',
        'USER': 'tdesai',
        'PASSWORD': '#ToBollywood',
        'HOST': 'fordemo.c91e6955bgwn.us-west-2.rds.amazonaws.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306'

    },
    '2010': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'Data_2010',
        'USER': 'tdesai',
        'PASSWORD': '#ToBollywood',
        'HOST': 'fordemo.c91e6955bgwn.us-west-2.rds.amazonaws.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306'

    },
    '2009': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'Data_2009',
        'USER': 'tdesai',
        'PASSWORD': '#ToBollywood',
        'HOST': 'fordemo.c91e6955bgwn.us-west-2.rds.amazonaws.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306'

    },
    'user':{
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'Data_Users',
        'USER': 'tdesai',
        'PASSWORD': '#ToBollywood',
        'HOST': 'fordemo.c91e6955bgwn.us-west-2.rds.amazonaws.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306'

    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]




