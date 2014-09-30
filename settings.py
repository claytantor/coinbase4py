import os

from ConfigParser import RawConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(__file__)
CONF_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STATIC_MAIN_DIR = os.path.join(PROJECT_DIR, '..', 'static/')


here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)

# you will need to copy the example and make custom
# settings for the environment
config = RawConfigParser()

#place in a dir that is not managed in the code base
# print 'config dir: {0}/conf/gitpatron_settings.ini'.format(CONF_DIR)
config.read('{0}/conf/gitpatron_settings.ini'.format(CONF_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('secrets','DJANGO_SECRET_KEY')
GITPATRON_PW_SECRET_KEY = config.get('secrets','GITPATRON_PW_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get('debug','DEBUG')

TEMPLATE_DEBUG = config.get('debug','TEMPLATE_DEBUG')

ENVIRONMENT = config.get('base','ENVIRONMENT')

ALLOWED_HOSTS = []
