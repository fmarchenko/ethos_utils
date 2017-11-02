# -*- coding: utf-8 -*-

import asyncio

from . import logger as watchers_logger

logger = watchers_logger.getChild(__name__)


class BaseWatcher(object):
    def __init__(self, *args, **kwargs):
        super(BaseWatcher, self).__init__()

    def run(self, *args, **kwargs):
        pass

    async def minestop(self):
        await self.run_command_shell('/opt/ethos/bin/minestop')

    async def run_command_shell(self, command):
        """Run command in subprocess (shell)

        Note:
            This can be used if you wish to execute e.g. "copy"
            on Windows, which can only be executed in the shell.
        """
        # Create subprocess
        process = await asyncio.create_subprocess_shell(command,
                                                        stdout=asyncio.subprocess.PIPE)

        # Status
        logger.debug(' '.join(('Started:', command, '(pid = ' + str(process.pid) + ')')))

        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()

        # Progress
        if process.returncode == 0:
            logger.debug(' '.join(('Done:', command, '(pid = ' + str(process.pid) + ')')))
        else:
            logger.debug(' '.join(('Failed:', command, '(pid = ' + str(process.pid) + ')')))

        # Result
        result = stdout.decode().strip()

        # Return stdout
        return result

    async def run_command(self, *args):
        """Run command in subprocess

        Example from:
            http://asyncio.readthedocs.io/en/latest/subprocess.html
        """
        # Create subprocess
        process = await asyncio.create_subprocess_exec(
            *args,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE)

        # Status
        print('Started:', args, '(pid = ' + str(process.pid) + ')')

        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()

        # Progress
        if process.returncode == 0:
            print('Done:', args, '(pid = ' + str(process.pid) + ')')
        else:
            print('Failed:', args, '(pid = ' + str(process.pid) + ')')

        # Result
        result = stdout.decode().strip()

        # Return stdout
        return result
