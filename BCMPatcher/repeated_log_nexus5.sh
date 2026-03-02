#!/system/bin/sh
while true
do
    dhdutil -i wlan0 consoledump >> /data/local/tmp/log.txt
done
