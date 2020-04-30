#!/bin/bash

BLOG_PATH="/www/hexo_site/source/_posts"

FILE_COUNT=`cd $BLOG_PATH && ls | grep -w $1 | wc -l`

if [ $FILE_COUNT -eq 0 ]; then
    echo "Can't find $1" >> ./del_blog.log
    exit 1
else
    mv $BLOG_PATH/$1 $BLOG_PATH/'del_'$1'.bak'
    echo "Remove success $BLOG_PATH/$1" >> ./del_blog.log
fi
