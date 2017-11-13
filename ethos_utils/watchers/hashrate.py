# -*- coding: utf-8 -*-

import asyncio
import re

from ethos_utils.watchers.base import BaseWatcher
from ethos_utils.watchers import logger as watchers_logger

logger = watchers_logger.getChild(__name__.split('.')[-1])


class HashrateWatcher(BaseWatcher):
    def __init__(self, min_hashrate=22*12, attempt_sleep=60, **kwargs):
        self._min_hashrate = float(min_hashrate)
        self._attempt_sleep = int(attempt_sleep)

    def need_reboot(self):
        hashrate = float(re.split(r'^hash:', self.stats, flags=re.MULTILINE)[1].split('\n')[0].strip())
        logger.info('hash - {}, minimal - {}'.format(hashrate, self._min_hashrate))
        return hashrate < self._min_hashrate
