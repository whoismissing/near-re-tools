#!/system/bin/sh

#Fixing up the debug_info_ptrs, since Broadcom forgot to add the location 
#of the magic HNDRTE_DEBUG_PTR_PTR_MAGIC value on the Nexus 6P, which causes
#dhdutil to fail when trying to dump the console!
#This patch allows "consoledump" to work correctly
dhdutil -i wlan0 membytes -h 0x1800f8 8 4442505018841e00
while true
do
	#Directly reading the log buffer instead of going through all the hoops...
	#This is needed because the BCM4358 is so fast that the buffer wraps around
	#nearly immediately
	dhdutil -i wlan0 membytes -r 0x23dab4 0x400 >> /data/local/tmp/log.txt
done
