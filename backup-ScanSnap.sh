#!/bin/sh
#
MYNAME=`basename $0`

DST_DIR=/common/Win/Scan/_tmp

VENVDIR=$HOME/env3-gdrive
VENV_SUBDIR=gdrive-client


exec $VENVDIR/$VENV_SUBDIR/gdrive-client.sh $VENVDIR ScanSnap -dl $DST_DIR
