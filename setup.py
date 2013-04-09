# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='django-apiview',
    version='1.0.0',
    author=u'David Horn',
    author_email='david@d8a.me',
    packages=['django'],
    url='https://github.com/Madrox/django-apiview',
    license='MIT license. See http://opensource.org/licenses/MIT',
    description='A lightweight decorator to make it easy to create json-based API views in django',
    long_description='A lightweight decorator to make it easy to create json-based API views in django. It should abstract away most of the common input and output scrubbing.',
    zip_safe=True,
)