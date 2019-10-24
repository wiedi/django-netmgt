import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'sb$z85@ix+!ur1wcl8ua)4-#iqr*5&)r$!+w@#r)zw&ifb1x=#'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'rest_framework',
	'netmgt',
)

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

TEMPLATES = [
{
	'BACKEND': 'django.template.backends.django.DjangoTemplates',
	'DIRS': [os.path.join(BASE_DIR,'templates')],
	'APP_DIRS': True,
	'OPTIONS': {
		'context_processors': [
			'django.template.context_processors.debug',
			'django.template.context_processors.request',
			'django.contrib.auth.context_processors.auth',
			'django.contrib.messages.context_processors.messages',
		],
	},
},]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'


# DRF
REST_FRAMEWORK = {
	'DEFAULT_RENDERER_CLASSES': [
		'rest_framework.renderers.JSONRenderer',
		'rest_framework.renderers.BrowsableAPIRenderer',
	]
}


# NETMGT

NETMGT_DEFAULT_TTL = 3600
NETMGT_DEFAULT_NAMESERVERS_TTL = 86400
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
NETMGT_DNS_TOKEN = 'secure'
NETMGT_EXPORT_PREFIX = 'core'
