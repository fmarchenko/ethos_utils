import logging

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Nov 01, 2017"

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
