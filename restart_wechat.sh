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
MAX_REQUESTS=40
USER=nginx
GROUP=nginx
ERROR_LOG=/data/logs/gunicorn/wechat_error.log
# stop
for pid in `ps -ef|grep $GUNICORN_EXEC|grep $WSGI_NAME|grep -v grep| awk '$3 ==1 {print $2}'`
do
    kill $pid
done

# start
nohup $GUNICORN_EXEC $WSGI_NAME -b $LISTEN -w $WORKERS -u $USER -g $GROUP --worker-connections $WORKERCONNECTIONS -t $TIMEOUT --keep-alive $KEEPALIVE -D --access-logfile $ACCESS_LOG --error-logfile $ERROR_LOG 2>&1 &
