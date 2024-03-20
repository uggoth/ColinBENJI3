#!/bin/sh
echo Starting
echo Starting >> /home/pi/aaa.log
rm /home/pi/aaa.log
sleep 10   #  Must allow time for mysql, pigpiod, etc. etc. to get going
touch /home/pi/aaa.log
#
echo Checking DIPs
pigs m 20 r
pigs pud 20 u
dip_3=`pigs r 20`
echo DIP_3 $dip_3 >> /home/pi/aaa.log
echo DIP_3 $dip_3
#
pigs m 21 r
pigs pud 21 u
dip_4=`pigs r 21`
echo DIP_4 $dip_4 >> /home/pi/aaa.log
echo DIP_4 $dip_4
#
if [ $dip_4 != 1 ]; then
	echo Running Main >> /home/pi/aaa.log
	echo Running Main
	nohup python3 /home/pi/ColinThisPi/main_rc_zombie_arm_v03.py &
	echo Running MJPEG >> /home/pi/aaa.log
	echo Running MJPEG
	nohup python3 /home/pi/ColinThisPi/mjpeg_server_v02.py &
fi
sleep 3
disown
sleep 3
