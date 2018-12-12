# If you want the Bartberry Pi to load automatically on boot:
# 1) Place this file in /home/pi
# 2) Add the following line of code to /etc/rc.local: /usr/bin/python /home/pi/boot.py &
# 3) Before you save and quit, make sure the ampersand is at the end of the line of code, or you could brick your pi!!
# 4) Save and reboot (I think your pi needs to be configured to boot to the CLI by default, not the GUI-based OS, but I don't know for sure)

import os
from time import sleep

sleep(5)

os.system('cd /home/pi/Desktop/BARTBERRY_PI;python3 BARTBERRY_PI.py')
os.system('python3 BARTBERRY_PI.py')
