from distutils.core import setup

setup(
    name='coinbase4py',
    version='0.2.1',
    packages=['lib'],
    package_data={'coinbase4py': ['ca_certs.txt']},
    url='https://github.com/claytantor/coinbase4py',
    license='Apache License Version 2.0',
    author='Clay Graham',
    author_email='claytantor@gmail.com',
    description='Integration Library for the Coinbase API',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'httplib2>=0.9',
    ],

)