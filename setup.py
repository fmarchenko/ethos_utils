#!/usr/bin/env python

from setuptools import setup

setup(name='EthOS Utils', version='1.0',
      description='EthOS Utilities',
      author='Fedor Marchenko',
      author_email='mfs90@mail.ru',
      packages=['ethos_utils', 'ethos_utils.watchers'],
      scripts=['bin/watchmine']
)
