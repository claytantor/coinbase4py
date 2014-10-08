import os

from ConfigParser import RawConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(__file__)
CONF_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)

# you will need to copy the example and make custom
# settings for the environment
config = RawConfigParser()

#place in a dir that is not managed in the code base
# print 'config dir: {0}/conf/gitpatron_settings.ini'.format(CONF_DIR)
config.read('{0}/conf/coinbase4py_settings.ini'.format(CONF_DIR))
print 'loading config file: {0}/conf/coinbase4py_settings.ini'.format(CONF_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('secrets','DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get('debug','DEBUG')

TEMPLATE_DEBUG = config.get('debug','TEMPLATE_DEBUG')

ENVIRONMENT = config.get('base','ENVIRONMENT')


ALLOWED_HOSTS = []

#the database for the app
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'coinbase4py.db'),
    }
}

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'coinbase4py',

)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.request",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.tz",
                               "django.contrib.messages.context_processors.messages")

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'webapp.urls'

WSGI_APPLICATION = 'webapp.wsgi.application'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''


# Additional locations of static files
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, '../', 'static/'),
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

print PROJECT_DIR
TEMPLATE_DIRS = (
    PROJECT_DIR + '/../webapp/templates/',
)

USER_ONE=config.get('coinbase4py','USER_ONE')
USER_TWO=config.get('coinbase4py','USER_TWO')
TEST_STATE_DIR=config.get('coinbase4py','TEST_STATE_DIR')

COINBASE_OAUTH_CLIENT_APP=config.get('coinbase','COINBASE_OAUTH_CLIENT_APP')
COINBASE_OAUTH_CLIENT_ID=config.get('coinbase','COINBASE_OAUTH_CLIENT_ID')
COINBASE_OAUTH_CLIENT_SECRET=config.get('coinbase','COINBASE_OAUTH_CLIENT_SECRET')
COINBASE_OAUTH_CLIENT_CALLBACK=config.get('coinbase','COINBASE_OAUTH_CLIENT_CALLBACK')