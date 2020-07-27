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

        try:
            self._gauth = GoogleAuth()
        except Exception as e:
            self._debug('%s:%s', type(e), e)
            
        self._gauth.LocalWebserverAuth()

        self._drv = GoogleDrive(self._gauth)

    def main(self):
        self._log.debug('')

        top_id = self.get_folder_id('ScanSnap')
        if len(top_id) == 0:
            self._log.error('???')
            return

        self.get_list(top_id)

    def get_folder_id(self, folder_name):
        """
        get_folder_id
        """
        self._log.debug('folder_name=%s', folder_name)

        ids = self._drv.ListFile({'q': "title='%s'" % folder_name}).GetList()
        if len(ids) != 1:
            self._log.error('???')
            return ''

        return ids[0]['id']

    def get_list(self, id):
        """
        get_list
        """
        self._log.debug('id=%s', id)

        try:
            flist = self._drv.ListFile({
                'q':
                '"%s" in parents and trashed = false' % id
            }).GetList()
        except Exception as ex:
            self._debug('%s:%s', type(ex), ex)
        if flist == []:
            self._log.error('???')
            return []

        for f in flist:
            print('%s (%s)' % (f['title'], f['mimeType']))

            if f['mimeType'] == 'application/vnd.google-apps.folder':
                self.get_list(f['id'])


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
