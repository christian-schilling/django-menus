#!/usr/bin/python
from setuptools import setup, find_packages

setup(
    name='django-menus',
    version='0.0.1',
    description='per object permissions for Django',
    author='Christian Schilling',
    author_email='initcrash@gmail.com',
    url='http://github.com/initcrash/django-menus/',
    download_url='http://github.com/initcrash/django-menus/downloads',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
    packages=[ 'menus','menus.templatetags' ],
    package_data={'menus':['templates/menus/*.html']},
)

