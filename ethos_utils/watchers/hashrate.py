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
    def run(self, *args, **kwargs):
        yield from super(HashrateWatcher, self).run(*args, **kwargs)
        attempt = 0
        while attempt < 2:
            try:
                hashrate = float(re.split(r'^hash:', self.stats, flags=re.MULTILINE)[1].split('\n')[0].strip())
                logger.info('hash - {}, minimal - {}'.format(hashrate, self._min_hashrate))
                if hashrate < self._min_hashrate:
                    if attempt == 0:
                        attempt += 1
                        yield from asyncio.sleep(self._attempt_sleep)
                        continue
                    logger.info('run minestop')
                    yield from self.minestop()
            except Exception as ex:
                logger.error(ex)
                if attempt == 0:
                    attempt += 1
                    yield from asyncio.sleep(self._attempt_sleep)
                    continue
                logger.info('run minestop')
                yield from self.minestop()
            attempt += 2
