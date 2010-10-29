#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    print '(WARNING: importing distutils, not setuptools!)'
    from distutils.core import setup

setup(name='debrujinator',
      version='0.1',
      description='A basic de Brujin graph implementation',
      author='Russell Neches',
      author_email='ryneches@ucdavis.edu',
      url='',
      packages=['debrujinator', 'debrujinator.tests'],
      package_data={'debrujinator.tests': ['stap_16S.fa', 'query.fa']},
      license='BSD',
      test_suite = 'nose.collector'
      )
