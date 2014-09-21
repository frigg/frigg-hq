#!/bin/bash
set -e
NUM_WORKERS=8

. .environment

LOGDIR=$(dirname $LOGFILE)
ADDRESS=127.0.0.1:$PORT
cd $PROJECT_PATH 
source $PROJECT_PATH/venv/bin/activate
test -d $LOGDIR || mkdir -p $LOGDI

exec gunicorn frigg.wsgi:application -w $NUM_WORKERS --bind=$ADDRESS \
  --user=$USER --group=$GROUP --log-level=debug \
  --log-file=$LOGFILE 2>>$LOGFILE
