# -*- coding: utf-8 -*-

import asyncio
import re

from ethos_utils.watchers import logger as watchers_logger

logger = watchers_logger.getChild(__name__.split('.')[-1])


class BaseWatcher(object):
    _attempt = 0
    _attempt_sleep = 60

    def __init__(self, *args, **kwargs):
        super(BaseWatcher, self).__init__()

    @asyncio.coroutine
    def run(self, *args, **kwargs):
        self.stats = yield from self.run_command_shell('/opt/ethos/bin/stats')
        self.status = re.split(r'^status:', self.stats, flags=re.MULTILINE)[1].split('\n')[0].strip()
        logger.info('Status: {}'.format(self.status))

        while self._attempt < 2:
            try:
                if self.need_reboot():
                    if self._attempt < 1:
                        self._attempt += 1
                        yield from asyncio.sleep(self._attempt_sleep)
                        continue
                    logger.info('run minestop')
                    yield from self.minestop()
                self._attempt = 2
            except Exception as ex:
                logger.error(ex)
                yield from asyncio.sleep(self._attempt_sleep)
                continue
        self._attempt = 0

    def gpu_crashed(self):
        return 'reboot required' in self.status

    def many_autoreboots(self):
        return 'too many autoreboots' in self.status

    def need_reboot(self):
        pass

    @asyncio.coroutine
    def minestop(self):
        if self.many_autoreboots():
            logger.info('Reset thermal-related throttling back to normal')
            yield from self.run_command_shell('/opt/ethos/bin/clear-thermals')
            return
        elif self.gpu_crashed():
            logger.info('Issue a regular reboot system')
            yield from self.run_command_shell('/opt/ethos/bin/r')
            return
        yield from self.run_command_shell('/opt/ethos/bin/minestop')

    @asyncio.coroutine
    def run_command_shell(self, command):
        """Run command in subprocess (shell)

        Note:
            This can be used if you wish to execute e.g. "copy"
            on Windows, which can only be executed in the shell.
        """
        # Create subprocess
        process = yield from asyncio.create_subprocess_shell(command,
                                                             stdout=asyncio.subprocess.PIPE
                                                             )

        # Status
        logger.debug(' '.join(('Started:', command, '(pid = ' + str(process.pid) + ')')))

        # Wait for the subprocess to finish
        stdout, stderr = yield from process.communicate()

        # Progress
        if process.returncode == 0:
            logger.debug(' '.join(('Done:', command, '(pid = ' + str(process.pid) + ')')))
        else:
            logger.debug(' '.join(('Failed:', command, '(pid = ' + str(process.pid) + ')')))

        # Result
        result = stdout.decode().strip()

        # Return stdout
        return result

    @asyncio.coroutine
    def run_command(self, *args):
        """Run command in subprocess

        Example from:
            http://asyncio.readthedocs.io/en/latest/subprocess.html
        """
        # Create subprocess
        process = yield from asyncio.create_subprocess_exec(*args,
                                                            # stdout must a pipe to be accessible as process.stdout
                                                            stdout=asyncio.subprocess.PIPE)

        # Status
        print('Started:', args, '(pid = ' + str(process.pid) + ')')

        # Wait for the subprocess to finish
        stdout, stderr = yield from process.communicate()

        # Progress
        if process.returncode == 0:
            print('Done:', args, '(pid = ' + str(process.pid) + ')')
        else:
            print('Failed:', args, '(pid = ' + str(process.pid) + ')')

        # Result
        result = stdout.decode().strip()

        # Return stdout
        return result
