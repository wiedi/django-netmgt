import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'sb$z85@ix+!ur1wcl8ua)4-#iqr*5&)r$!+w@#r)zw&ifb1x=#'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = (
	'suit',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'netmgt',
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

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
	'django.core.context_processors.request',
)

SUIT_CONFIG = {
	'ADMIN_NAME': 'Network Management Tool',
}

ROOT_URLCONF = 'netmgt_web.urls'
WSGI_APPLICATION = 'netmgt_web.wsgi.application'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
		'LOCATION': 'core_cache',
	}
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

# NETMGT

NETMGT_DEFAULT_TTL = 3600
NETMGT_DEFAULT_NAMESERVERS = [
	'ns1.example.com',
	'ns2.example.com',
	'ns3.example.com',
]
NETMGT_HOSTMASTER = 'hostmaster.example.com'
NETMGT_SOA = {
	'refresh': '2d',
	'retry':   '15M',
	'expiry':  '2w',
	'minimum': '1h',
}
