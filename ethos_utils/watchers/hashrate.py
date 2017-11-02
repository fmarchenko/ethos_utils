# -*- coding: utf-8 -*-

import asyncio

from .base import BaseWatcher
from . import logger as watchers_logger

logger = watchers_logger.getChild(__name__)


class HashrateWatcher(BaseWatcher):
    def __init__(self, min_hashrate=22*12, attempt_sleep=60, **kwargs):
        self._min_hashrate = float(min_hashrate)
        self._attempt_sleep = int(attempt_sleep)

    async def run(self):
        attempt = 0
        while attempt < 2:
            with open('/var/run/ethos/status.file', 'r') as fin:
                status_file = fin.read().strip()
            try:
                hashrate = float(status_file.split(':')[0].split(' ')[0].strip())
                logger.info('Hashrate watcher: hash - {}, minimal - {}'.format(hashrate, self._min_hashrate))
                if hashrate < self._min_hashrate:
                    if attempt == 0:
                        attempt += 1
                        await asyncio.sleep(self._attempt_sleep)
                        continue
                    await self.minestop()
            except Exception as ex:
                logger.error(ex)
                logger.error(status_file)
                if attempt == 0:
                    attempt += 1
                    await asyncio.sleep(self._attempt_sleep)
                    continue
                await self.minestop()
            attempt += 2