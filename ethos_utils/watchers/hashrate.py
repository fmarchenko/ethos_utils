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

    @asyncio.coroutine
    def run(self):
        attempt = 0
        while attempt < 2:
            try:
                self.stats = yield from self.run_command_shell('/opt/ethos/bin/stats')
                hashrate = float(re.split(r'^hash:', self.stats, flags=re.MULTILINE)[1].split('\n')[0].strip())
                logger.info('Hashrate watcher: hash - {}, minimal - {}'.format(hashrate, self._min_hashrate))
                if hashrate < self._min_hashrate:
                    if self.gpu_crashed():
                        yield from self.run_command_shell('/opt/ethos/bin/r')
                    if attempt == 0:
                        attempt += 1
                        yield from asyncio.sleep(self._attempt_sleep)
                        continue
                    yield from self.minestop()
            except Exception as ex:
                logger.error(ex)
                if attempt == 0:
                    attempt += 1
                    yield from asyncio.sleep(self._attempt_sleep)
                    continue
                yield from self.minestop()
            attempt += 2

    def gpu_crashed(self):
        status = self.stats.split('status:')[1].split('\n')[0]
        logger.info('Hashrate wather: status {}'.format(status))
        return 'reboot required' in status
