# Django settings for researchhub project.
import os
import sys
import django.conf.global_settings as DEFAULT_SETTINGS

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_PARENT_DIR = os.path.dirname(PROJECT_ROOT)

PROJECT_MODULE = __name__[:__name__.rfind('.')] if '.' in __name__ else PROJECT_ROOT.split(os.sep)[-1]

LOG_DIR = os.path.join(PROJECT_PARENT_DIR, 'logs')

#Append the apps/ directory to the path so all our apps can be grouped together there.
sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': os.path.join(PROJECT_ROOT, 'foo'),					  # Or path to database file if using sqlite3.
		'USER': '',					  # Not used with sqlite3.
		'PASSWORD': '',				  # Not used with sqlite3.
		'HOST': '',					  # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',					  # Set to empty string for default. Not used with sqlite3.
	}
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PARENT_DIR, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PARENT_DIR, "collected_static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
	# Put strings here, like "/home/html/static" or "C:/www/django/static".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(PROJECT_PARENT_DIR, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#	'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'qg9$l-&amp;))h(152tp5iq6w=$9oi20s071c8^8uq5bo62&amp;80&amp;h1c'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
#	 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
	# Uncomment the next line for simple clickjacking protection:
	# 'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = PROJECT_MODULE+'.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'researchhub.wsgi.application'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(PROJECT_ROOT, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
	'django.core.context_processors.request',
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'django.contrib.admindocs',
	#3rd Party Apps
	'debug_toolbar',
	'django_extensions',
	'django_config_gen',
	'django_email_test',
	'memcache_status',
	'registration',
	'south',
	#Project Apps
	'researchhub_app',
)

#LOGGING CONFIGURATION##########################################################
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {#http://docs.python.org/library/logging.html#logrecord-attributes
		'verbose_color': {
			'()': 'logging.ColorFormatter',
			'format': '$BOLD$COLOR%(levelname)s$RESET %(asctime)s %(process)d %(thread)d %(name)s:%(lineno)s %(funcName)s() %(message)s'
		},
		'verbose_sql_color': {
			'()': 'logging.ColorFormatter',
			'format': '$BOLD$COLOR%(levelname)s$RESET %(asctime)s %(process)d %(thread)d %(name)s:%(lineno)s %(funcName)s() %(message)s %(duration)s %(sql)s %(params)s'
		},
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(process)d %(thread)d %(name)s:%(lineno)s %(funcName)s() %(message)s'
		},
		'verbose_sql': {
			'format': '%(levelname)s %(asctime)s %(process)d %(thread)d %(name)s:%(lineno)s %(funcName)s() %(message)s %(duration)s %(sql)s %(params)s'
		},
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'class': 'django.utils.log.AdminEmailHandler',
		},
		'file': {
			'class': 'logging.handlers.TimedRotatingFileHandler',
			'level': 'DEBUG',
			'formatter': 'verbose',
			'filename': os.path.join(LOG_DIR, 'django.log'),#TODO: use process id
			'when': 'midnight',
			'backupCount': 5,
		},
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'verbose_color',
		},
		'console_sql': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'verbose_sql_color',
		},
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
		'django': {
			'handlers': ['console'],
			'level': 'DEBUG',
			'propagate': True,
		},
		'django_query_caching': {
			'level': 'WARNING',
			'propagate': True,
		},
		'django.db.backends': {
			'handlers': [],#'console_sql'],
			'level': 'DEBUG',
			'propagate': False,
		},
		'south': {
			'level': 'INFO',
		},
	},
	'root': {
		'handlers': ['console'],
		'level': 'DEBUG',
	}
}
#south logging bug workaround
import logging
import south.logger
logging.getLogger('south').setLevel(logging.INFO)

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
	'WARNING'  : YELLOW,
	'INFO'	 : WHITE,
	'DEBUG'	: BLUE,
	'CRITICAL' : YELLOW,
	'ERROR'	: RED,
	'RED'	  : RED,
	'GREEN'	: GREEN,
	'YELLOW'   : YELLOW,
	'BLUE'	 : BLUE,
	'MAGENTA'  : MAGENTA,
	'CYAN'	 : CYAN,
	'WHITE'	: WHITE,
}

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ  = "\033[1m"

#http://stackoverflow.com/questions/384076/how-can-i-make-the-python-logging-output-to-be-colored/2532931#2532931
class ColorFormatter(logging.Formatter):
	def __init__(self, *args, **kwargs):
		# can't do super(...) here because Formatter is an old school class
		logging.Formatter.__init__(self, *args, **kwargs)

	def format(self, record):
		levelname = record.levelname
		color	 = COLOR_SEQ % (30 + COLORS[levelname])
		message   = logging.Formatter.format(self, record)
		message   = message.replace("$RESET", RESET_SEQ)\
						   .replace("$BOLD",  BOLD_SEQ)\
						   .replace("$COLOR", color)
		for k,v in COLORS.items():
			message = message.replace("$" + k,	COLOR_SEQ % (v+30))\
							 .replace("$BG" + k,  COLOR_SEQ % (v+40))\
							 .replace("$BG-" + k, COLOR_SEQ % (v+40))
		return message + RESET_SEQ

logging.ColorFormatter = ColorFormatter

#END LOGGING CONFIGURATION######################################################

CONFIG_GEN_TEMPLATES_DIR = os.path.join(PROJECT_PARENT_DIR, 'config', 'templates')
CONFIG_GEN_GENERATED_DIR = os.path.join(PROJECT_PARENT_DIR, 'config', 'generated')

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
	from local_settings import *
except ImportError:
	pass

#if manage.py test was called, use test settings
if 'test' in sys.argv:
	try:
		from test_settings import *
	except ImportError:
		pass

#DEBUG mode settings
if DEBUG == True:
	
	#only use FirePython if runserver is used, since it causes problems when proxying through Nginx (DEBUG=True on staging server)
	if 'runserver' in sys.argv or 'runserver_plus' in sys.argv:
		MIDDLEWARE_CLASSES += ('firepython.middleware.FirePythonDjango',)
	
	DEBUG_TOOLBAR_CONFIG = {
		'INTERCEPT_REDIRECTS': False,
	}
	
	#To see all logging messages. Can switch to new method with Django 1.3
	import logging
	logging.getLogger('').setLevel(logging.DEBUG)
	logging.getLogger('django_query_caching').setLevel(logging.WARNING)
	#we need to log something here, or else other logging messages won't show up later, but we don't want to log anything when using tab completion
	if len(sys.argv) > 1:
		logging.debug('logging enabled')
else:
	#if not debugging, cache the templates
	TEMPLATE_LOADERS = (
		('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
	)
	TEMPLATE_DEBUG = False
