#!/usr/bin/env python3
#
# (c) 2022 Yoichi Tanibayashi
#
"""
"""

import os
import sys
import time
import datetime
import subprocess
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import click
from MyLogger import get_logger, WARNING, ERROR
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


MYNAME = 'gdrv_check_folder'
VERSION = '0.1.1'

class Gdrv:
    """ Gdrv """
    _log = get_logger(__name__, False)

    DEF_LOOP_INTERVAL = 15

    def __init__(self, debug=WARNING):
        self._dbg = debug
        __class__._log = get_logger(__class__.__name__, self._dbg)
        self._log.debug('')

        try:
            self._gauth = GoogleAuth()
        except Exception as e:
            self._debug('%s:%s', type(e), e)
            sys.exit(0)
        self._gauth.LocalWebserverAuth()
        self._drv = GoogleDrive(self._gauth)

        self._flist = []

    def check_folder(self, folder, cmd_add='', cmd_remove=''):
        self._log.debug('folder=%a', folder)

        # ts_str: Time Stamp String: 'yyyy-mm-dd HH:MM:SS'
        ts_str = '%s' % datetime.datetime.now()
        ts_str = ts_str[0:19]

        # q_str: Querry string for gdrive
        q_str = "'%s' in parents" % folder
        q_str += ' and trashed=false'
        self._log.debug('q_str=%a', q_str)
        q = {'q': '%s' % q_str}
        self._log.debug('q=%s', q)

        # flist: current file list from gdrive
        flist = self._drv.ListFile(q).GetList()
        self._log.debug('num of files=%d', len(flist))

        dec_count = 0
        inc_count = 0

        # title_list: current title list
        title_list = []
        for f in flist:
            title_list.append(f['title'])
        self._log.debug('title_list: %s', title_list)

        new_title_list = []
        new_flist = []
        for f in self._flist:
            if f['title']  in title_list:
                new_flist.append(f)
                new_title_list.append(f['title'])
            else:
                msg = '%s> remove %s' % (ts_str, f['title'])
                print(msg)
                dec_count += 1
                if ( len(cmd_remove) > 0 ):
                    args = [cmd_remove] + msg.split()
                    print('args=%s' % args)
                    subprocess.call(args)
        self._log.debug('dec_count=%d', dec_count)

        for f in flist:
            if f['title'] not in new_title_list:
                new_flist.append(f)
                inc_count += 1
                msg = '%s> add %s' % (ts_str, f['title'])
                print(msg)
                if ( len(cmd_add) > 0 ):
                    args = [cmd_add] + msg.split()
                    subprocess.call(args)
        self._log.debug('inc_count=%d', inc_count)

        self._flist = new_flist

    def loop(self, folder, interval=DEF_LOOP_INTERVAL,
             cmd_add='', cmd_remove=''):
        while True:
            self.check_folder(folder, cmd_add, cmd_remove)
            time.sleep(interval)



@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('folder')
@click.option('--interval', '-s', 'interval', type=int,
              default=Gdrv.DEF_LOOP_INTERVAL,
              help='interval sec (default: %s sec)' % Gdrv.DEF_LOOP_INTERVAL)
@click.option('--cmd_add', '-a', 'cmd_add', type=str, default='',
              help='command (add)')
@click.option('--cmd_remove', '-r', 'cmd_remove', type=str, default='',
              help='command (remove)')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(folder, interval, cmd_add, cmd_remove, debug):
    _log = get_logger(__name__, debug)
    _log.debug('folder=%s, interval=%d', folder, interval)
    _log.debug('cmd_add=%s', cmd_add)
    _log.debug('remove=%s', cmd_remove)

    gdrv = Gdrv(debug=debug)
    try:
        gdrv.loop(folder, interval, cmd_add, cmd_remove)
    finally:
        _log.debug('end')


if __name__ == "__main__":
    main()
