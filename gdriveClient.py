#!/usr/bin/env python3
#
# (c) Yoichi Tanibayashi
#
"""
"""
__author__ = 'Yoichi Tanibayashi'
__date__   = '2020/07'

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import click
from MyLogger import get_logger
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


MYNAME = 'gdriveClient'
VERSION = '0.00'


class ClassApp:
    _log = get_logger(__name__, False)

    def __init__(self, debug=False):
        self._dbg = debug
        __class__._log = get_logger(__class__.__name__, self._dbg)
        self._log.debug('')

        self._gauth = GoogleAuth()
        self._gauth.LocalWebserverAuth()

        self._drive = GoogleDrive(self._gauth)

    def main(self):
        self._log.debug('')
        


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(debug):
    _log = get_logger(__name__, debug)
    _log.info('')

    app = ClassApp(debug=debug)
    try:
        app.main()
    finally:
        _log.info('end')


if __name__ == "__main__":
    main()

