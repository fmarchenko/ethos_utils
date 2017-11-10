import os
import logging
import configparser

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Nov 01, 2017"

config = configparser.ConfigParser()
config.read(['defaults.ini', os.path.expanduser('~/.ethos_utils.ini')])
config_logging = config['logging']

logger = logging.getLogger(__name__)
logger.setLevel(level=logging._nameToLevel[config_logging.get('level', 'INFO').upper()])
fmt = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(name)-15s: %(message)s')

if config_logging.get('type', 'stream').upper() == 'FILE':
    ch = logging.FileHandler(filename=config_logging.get('log_file', '/var/log/ethos_utils/ethos_utils.log'))
else:
    ch = logging.StreamHandler()

ch.setLevel(level=logging._nameToLevel[config_logging.get('level', 'INFO').upper()])
ch.setFormatter(fmt)
logger.addHandler(ch)
