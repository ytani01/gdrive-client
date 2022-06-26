#!/bin/sh
#
MYNAME=`basename $0`

SRC_DIR=ScanSnap
#YEAR=`date +%Y`
DST_DIR=/common/Win/Scan/_tmp
echo "DST_DIR=$DST_DIR"

VENVDIR=$HOME/env8-gdrive
VENV_SUBDIR=gdrive-client


exec $VENVDIR/$VENV_SUBDIR/gdrive-client.sh $VENVDIR $SRC_DIR -dl $DST_DIR
