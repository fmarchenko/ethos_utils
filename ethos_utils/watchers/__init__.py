from ethos_utils import logger as ethos_utils_logger
logger = ethos_utils_logger.getChild(__name__.split('.')[-1])

from .base import BaseWatcher

__all__ = ['base',
    'temperature',
    'hashrate'
]
