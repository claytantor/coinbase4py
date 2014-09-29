#!/usr/bin/env python

import sys
import os
from setuptools import setup, find_packages

_top_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_top_dir, "lib"))
try:
    import markdown_deux
finally:
    del sys.path[0]
README = open(os.path.join(_top_dir, 'README.md')).read()

setup(name='coinbase4py',
    version=markdown_deux.__version__,
    description="a Django app that provides a client to coinbase.com)",
    long_description=README,
    classifiers=[c.strip() for c in """
        Development Status :: 5 - Production/Stable
        Environment :: Web Environment
        Framework :: Django
        Intended Audience :: Developers
        License :: OSI Approved :: Apache License Version 2.0
        Operating System :: OS Independent
        Programming Language :: Python :: 2
        Topic :: Internet :: WWW/HTTP
        """.split('\n') if c.strip()],
    keywords='django client to coinbase.com',
    author='Clay Graham',
    author_email='claytantor@gmail.com',
    maintainer='Clay Graham',
    maintainer_email='claytantor@gmail.com',
    url='https://github.com/claytantor/coinbase4py',
    license='Apache License Version 2.0',
    install_requires = [],
    packages=["coinbase4py"],
    package_dir={"": "lib"},
    include_package_data=True,
    zip_safe=False,
)