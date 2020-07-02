# myrpi
INSTALLATION
sudo apt-get install wakeonlan

CRONTAB - cmd: crontab -e

*/5 * * * * TS_SOCKET=/tmp/taskbt tsp timeout 200 python3 /home/pi/myrpi/mi_thermo.py
@reboot python3 /home/pi/myrpi/flask_basic.py

CRONTAB admin

* 1 * * * sudo reboot
