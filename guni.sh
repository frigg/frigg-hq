#!/bin/bash
set -e
LOGFILE=/opt/frigg/guni.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=8
USER=ubuntu
GROUP=ubuntu
ADDRESS=127.0.0.1:8010
cd /opt/frigg
source /opt/frigg/venv/bin/activate
test -d $LOGDIR || mkdir -p $LOGDI
#export NEW_RELIC_CONFIG_FILE=newrelic.ini
exec gunicorn frigg.wsgi:application -w $NUM_WORKERS --bind=$ADDRESS \
  --user=$USER --group=$GROUP --log-level=debug \
  --log-file=$LOGFILE 2>>$LOGFILE