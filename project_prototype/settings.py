"""
Django settings for project_prototype project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_x$y2pqx#7&p8kl*#5=2t%)%aq*6#mxw6v4cu_y@fnw2ley9@3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'SecureWitness',
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

ROOT_URLCONF = 'project_prototype.urls'

WSGI_APPLICATION = 'project_prototype.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'SW_db',
		 #'USER': '', 
         #'PASSWORD': '',
         #'HOST': 'localhost', # '127.0.0.1' probably works also
         #'PORT': '5432',
    }
}

if os.getcwd() == "/app":
   DATABASES['default'] =  dj_database_url.config(default= "postgres://fglfuapozpgloe:u-teZQQ3jolevLq4L9gKYCa0J-@ec2-54-163-238-96.compute-1.amazonaws.com:5432/d98etkvq44eb9e")
   
# =======
# # if os.getcwd() == "/app":
# #     DATABASES['default'] =  dj_database_url.config(default="postgres://daebabdykgebhb:BdkgL7uYdrMBNx0X5-nNYlbiJr@ec2-54-204-45-126.compute-1.amazonaws.com:5432/d5t6jijl4vcq81")
# >>>>>>> Stashed changes

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

LOGIN_URL = '/SecureWitness/login/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

#STATIC_PATH = os.path.join(PROJECT_PATH, 'static')


STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    'static',
    #os.path.join(BASE_DIR, 'project_prototype/static'),
)

#Helps determine where to put the uploaded files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AUTH_PROFILE_MODULE = 'SecureWitness.UserProfile'


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'securewitness4@gmail.com'
EMAIL_HOST_PASSWORD = 'SecWit4jeec'
EMAIL_USE_TLS = True
