# -*- coding: utf-8 -*-

import asyncio
import re
from statistics import mean

from ethos_utils.watchers.base import BaseWatcher
from ethos_utils.watchers import logger as watchers_logger

logger = watchers_logger.getChild(__name__.split('.')[-1])


class TemperatureWatcher(BaseWatcher):
    _min_temp = 39

    def __init__(self, min_temp=39, attempt_sleep=60, **kwargs):
        self._min_temp = float(min_temp)
        self._attempt_sleep = int(attempt_sleep)

    def need_reboot(self):
        temps_bytes = re.split(r'^temp:', self.stats, flags=re.MULTILINE)[1].split('\n')[0].strip()
        avg_temp = mean([float(x) for x in str(temps_bytes).strip().split(' ')])
        logger.info('average - {}, minimal - {}'.format(avg_temp, self._min_temp))
        return avg_temp < self._min_temp
