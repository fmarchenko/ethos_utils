#!/usr/bin/env python

import os
import configparser
from setuptools import setup, find_packages

config = configparser.ConfigParser()
config.read(['defaults.ini', os.path.expanduser('~/.ethos_utils.ini')])
config_logging = config['logging']

log_file = config_logging.get('log_file', '/var/log/ethos_utils/ethos_utils.log')
logging_directory = os.path.dirname(log_file)

if not os.path.exists(logging_directory):
      os.makedirs(logging_directory)
with open(log_file, 'w+') as fout:
      fout.write('')
os.chmod(logging_directory, 0o777)
os.chmod(log_file, 0o666)

setup(name='EthOS Utils', version='1.0',
      description='EthOS Utilities',
      author='Fedor Marchenko',
      author_email='mfs90@mail.ru',
      packages=find_packages(),
      scripts=['bin/watchmine']
)
