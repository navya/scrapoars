#!/usr/bin/env python3
#
# File: setup.py
#
# Created: Sunday, July  6 2014 by rejuvyesh <mail@rejuvyesh.com>
# License: GNU GPL 3 <http://www.gnu.org/copyleft/gpl.html>
#

from setuptools import setup, find_packages

setup(name='scrapoars',
      version='0.1.0',
      licence='GPLv3',
      description='Scrape the crappy iit-k OARS website',
      url='http://github.com/rejuvyesh/scrapoars',
      author='rejuvyesh',
      author_email='mail@rejuvyesh.com',
      packages=find_packages(),
      entry_points={
        'console_scripts': ['scrapoars = scrapoars.cli:scrapoars']
      },
      install_requires=open('requirements.txt').readlines())
