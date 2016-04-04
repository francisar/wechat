#!/bin/bash

PYTHON_EXEC=/data/services/python/bin/python
WSGI_NAME=wechat.wsgi
GUNICORN_EXEC=/data/services/python/bin/gunicorn
LISTEN=127.0.0.1:38080
ACCESS_LOG=/data/logs/gunicorn/wechat_access.log
KEEPALIVE=20
WORKERS=5
TIMEOUT=120
WORKERCONNECTIONS=100
MAX-REQUESTS=40
# stop
for pid in `ps -ef|grep $GUNICORN_EXEC|grep $WSGI_NAME|grep -v grep| awk '$3 ==1 {print $2}'`
do
    kill $pid
done

# start
nohup $GUNICORN_EXEC $WSGI_NAME -b $LISTEN -w $WORKERS --worker-connections $WORKERCONNECTIONS -t $TIMEOUT     --max-requests $MAX-REQUESTS --keep-alive $KEEPALIVE -D --access-logfile $ACCESS_LOG 2>&1 &
