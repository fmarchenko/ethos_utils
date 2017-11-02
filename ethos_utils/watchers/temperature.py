# -*- coding: utf-8 -*-

import asyncio

from .base import BaseWatcher
from . import logger as watchers_logger

logger = watchers_logger.getChild(__name__)


class TemperatureWatcher(BaseWatcher):
    _min_temp = 39

    def __init__(self, min_temp=39, attempt_sleep=60, **kwargs):
        self._min_temp = float(min_temp)
        self._attempt_sleep = int(attempt_sleep)

    async def run(self):
        attempt = 0
        while attempt < 2:
            try:
                temps = [float(x) for x in str(await self.run_command_shell('/opt/ethos/bin/stats | grep ^temp | cut -d":" -f2')).strip().split(' ')]
            except ValueError:
                temps = [self._min_temp]
            avg_temp = sum(temps) / float(len(temps))
            logger.info('Temperature watcher: average - {}, minimal - {}'.format(avg_temp, self._min_temp))
            if avg_temp < self._min_temp:
                if attempt == 0:
                    attempt += 1
                    await asyncio.sleep(self._attempt_sleep)
                    continue
                await self.minestop()
            attempt += 2
