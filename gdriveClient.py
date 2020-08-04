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
import os

import click
from MyLogger import get_logger
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


MYNAME = 'gdriveClient'
VERSION = '0.00'


class ClassApp:
    _log = get_logger(__name__, False)

    def __init__(self, top_folder, dl_dst=None, debug=False):
        self._dbg = debug
        __class__._log = get_logger(__class__.__name__, self._dbg)
        self._log.debug('top_folder=%s dl_dst=%s',
                        top_folder, dl_dst)

        self._top_folder = top_folder
        self._dl_dst = dl_dst

        try:
            self._gauth = GoogleAuth()
        except Exception as e:
            self._debug('%s:%s', type(e), e)

        self._gauth.LocalWebserverAuth()

        self._drv = GoogleDrive(self._gauth)

    def main(self):
        self._log.debug('')

        top_id = self.get_folder_id(self._top_folder)
        if len(top_id) == 0:
            self._log.error('???')
            return

        self.get_list(self._top_folder, self._dl_dst, top_id)

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

    def get_list(self, folder_title='', dst=None, fid=None):
        """
        get_list
        """
        self._log.debug('folder_title=%s, dst=%s, fid=%s',
                        folder_title, dst, fid)

        if dst is not None:
            """
            make destination directory
            """
            try:
                os.mkdir('%s/%s' % (dst, folder_title))
            except FileExistsError as e:
                self._log.warning('%s', e)
            except Exception as e:
                self._log.error('%s:%s', type(e), e)
                return

        """
        get file list
        """
        try:
            flist = self._drv.ListFile({
                'q': '"%s" in parents and trashed = false' % fid
            }).GetList()
        except Exception as e:
            self._log.error('%s:%s', type(e), e)
            return

        if flist == []:
            self._log.error('???')
            return []

        """
        get files recursively
        """
        for f in flist:
            print('%s/%s (%s)' % (folder_title, f['title'], f['mimeType']))

            if f['mimeType'] == 'application/vnd.google-apps.folder':
                self.get_list('%s/%s' % (folder_title, f['title']),
                              dst,
                              f['id'])
            elif dst is not None:
                """
                download file
                """
                gf = self._drv.CreateFile({'id': f['id']})
                self._log.debug('gf=%s', gf)
                gf.GetContentFile('%s/%s/%s' % (dst, folder_title, f['title']))


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('top_folder')
@click.option('--download', '-dl', 'download', type=str, default='',
              help='download to destination directory')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(top_folder, download, debug):
    _log = get_logger(__name__, debug)
    _log.info('top_folder=%s, download=%s',
              top_folder, download)

    if download == '':
        download = None

    app = ClassApp(top_folder=top_folder, dl_dst=download, debug=debug)
    try:
        app.main()
    finally:
        _log.info('end')


if __name__ == "__main__":
    main()
