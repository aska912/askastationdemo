#!/usr/bin/bash

INSTALL_PATH="/opt/weixin"
PROJECT_OWNER=`getent passwd 1000 | cut -d ":" -f 1`
PROJECT_GROUP=`getent group 1002 | cut -d ":" -f 1`

if [ `whoami` != root ]; then
   echo "Please use root to install."
   exit 1 
fi

if [ -d $INSTALL_PATH ]; then
    echo "Please remove the original folder: $INSTALL_PATH"
    exit 1
fi

set -x

mkdir $INSTALL_PATH
cp -ra *.py $INSTALL_PATH
touch $INSTALL_PATH/access_token
chmod 755 $INSTALL_PATH/access_token
chmod 755 *.py
chown -R $PROJECT_OWNER:$PROJECT_GROUP $INSTALL_PATH

set +x
