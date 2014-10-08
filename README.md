coinbase4py
===========

python &amp; Django include project for anybody who wants to use coinbase.com


A small Django app that provides a client to coinbase.com


# Installation

- Get a git clone of the source tree:

        git clone https://github.com/claytantor/coinbase4py.git

    Then you'll need the "lib" subdir on your PYTHONPATH:

        cd coinbase4py
        python setup.py install


# Django project setup

1. Add `coinbase4py` to `INSTALLED_APPS` in your project's "settings.py".


# Setup a self signed cert
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mysitename.key -out mysitename.crt


# Configure apache
The coinbase API requires that your OAUTH callback is HTTPS, so configure your server 
to be open ssl and install the SSl cert.

    <VirtualHost coinbase4py.org:443>
     SSLEngine on
     SSLCertificateFile /home/ec2-user/keys/coinbase4py.crt
     SSLCertificateKeyFile /home/ec2-user/keys/coinbase4py.key
    </VirtualHost>


    (venv1)[ec2-user@ip-10-183-217-223 coinbase4py]$ python manage.py syncdb
    loading config file: /home/ec2-user/sites/conf/coinbase4py_settings.ini
    /home/ec2-user/sites/coinbase4py/webapp
    Creating tables ...
    Creating table django_admin_log
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group
    Creating table auth_user_groups
    Creating table auth_user_user_permissions
    Creating table auth_user
    Creating table django_content_type
    Creating table django_session

    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): yes
    Username (leave blank to use 'ec2-user'): coinbase4py
    Email address: foobar@gmail.com
    Password: 
    Password (again): 
    Superuser created successfully.
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)