coinbase4py
===========

python &amp; Django include project for anybody who wants to use coinbase.com


A small Django app that provides a client to coinbase.com


# Installation

- Get a git clone of the source tree:

        git clone git://github.com/trentm/django-markdown-deux.git

    You might want a particular tag:

        cd django-markdown-deux
        git tag -l   # list available tags
        git checkout $tagname

    Then you'll need the "lib" subdir on your PYTHONPATH:

        python setup.py install # or 'export PYTHONPATH=`pwd`/lib:$PYTHONPATH'

    You'll also need the [python-markdown2
    library](https://github.com/trentm/python-markdown2):

        git clone git@github.com:trentm/python-markdown2.git
        cd python-markdown2
        python setup.py install   # or 'export PYTHONPATH=`pwd`/python-markdown2/lib'


# Django project setup

1. Add `markdown_deux` to `INSTALLED_APPS` in your project's "settings.py".

2. Optionally set some of the `MARKDOWN_DEUX_*` settings. See the "Settings"
   section below.

