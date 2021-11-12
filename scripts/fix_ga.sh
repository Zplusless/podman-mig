# run in xrdp
cd /home/edge/gaminganywhere-master/bin
cp config/common/server-common.conf_bak config/common/server-common.conf 
sed -i "s/:0/$(echo $DISPLAY)/" config/common/server-common.conf 
# ./ga-server-periodic config/server.desktop.conf