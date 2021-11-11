cd /ga/bin 
sed -i "s/:0/$(echo $DISPLAY)/" config/common/server-common.conf 
./ga-server-periodic config/server.desktop.conf