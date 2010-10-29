#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    print '(WARNING: importing distutils, not setuptools!)'
    from distutils.core import setup

setup(name='debruijnator',
      version='0.1',
      description='A basic de Bruijn graph implementation',
      author='Russell Neches',
      author_email='ryneches@ucdavis.edu',
      url='',
      packages=['debruijnator', 'debrujinator.tests'],
      package_data={'debruijnator.tests': ['stap_16S.fa', 'query.fa']},
      license='BSD',
      test_suite = 'nose.collector'
      )
