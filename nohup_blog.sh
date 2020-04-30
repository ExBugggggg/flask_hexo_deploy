#!/bin/bash

HEXO_PID=`ps aux | grep hexo | grep -v grep | awk '{print $2}'`

# Your hexo root path
HEXO_PATH="/www/hexo_site"
# Your site logs path, create it first
HEXO_LOG_PATH="/www/logs/site_blog.log"

if [ "$HEXO_PID" == "" ]; then
    cd $HEXO_PATH && hexo g && nohup hexo s >> $HEXO_LOG_PATH 2>&1 &
    sleep 5s
    echo "success"
else
    for i in ${HEXO_PID[@]}
    do
        echo $i
    done
    cd $HEXO_PATH && hexo g && nohup hexo s >> $HEXO_LOG_PATH 2>&1 &
    sleep 5s
    echo "success"
fi