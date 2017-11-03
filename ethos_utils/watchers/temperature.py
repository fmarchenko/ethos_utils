# -*- coding: utf-8 -*-

import asyncio

from .base import BaseWatcher
from . import logger as watchers_logger

logger = watchers_logger.getChild(__name__.split('.')[-1])


class TemperatureWatcher(BaseWatcher):
    _min_temp = 39

    def __init__(self, min_temp=39, attempt_sleep=60, **kwargs):
        self._min_temp = float(min_temp)
        self._attempt_sleep = int(attempt_sleep)

    @asyncio.coroutine
    def run(self):
        attempt = 0
        while attempt < 2:
            try:
                temps_bytes = yield from self.run_command_shell('/opt/ethos/bin/stats | /bin/grep ^temp | /usr/bin/cut -d":" -f2')
                temps = [float(x) for x in str(temps_bytes).strip().split(' ')]
            except ValueError:
                temps = [self._min_temp]
            avg_temp = sum(temps) / float(len(temps))
            logger.info('Temperature watcher: average - {}, minimal - {}'.format(avg_temp, self._min_temp))
            if avg_temp < self._min_temp:
                if attempt == 0:
                    attempt += 1
                    yield from asyncio.sleep(self._attempt_sleep)
                    continue
                yield from self.minestop()
            attempt += 2
