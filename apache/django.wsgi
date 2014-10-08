import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
sys.path.append('/home/ec2-user/sites/coinbase4py')
