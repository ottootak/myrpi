import argparse
import yaml
from collections import namedtuple, defaultdict
from rf_driver import RFDevice

GPIOS = {433 : 25, 315 : 17}
FILE_PATH = "/home/pi/myrpi/devices.yaml"

parser = argparse.ArgumentParser(description = "Sends signal based on device name")
parser.add_argument('name', metavar='NAME', type=str,
		    help="Name of device from /home/pi/RF_DEVICES.txt")
args = parser.parse_args()


device = namedtuple('device', 'freq, dec, protocol, pulse, length, repeats')

with open(FILE_PATH, 'r') as stream:
	try:
		cfg = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
            print(exc)

try:
	a = cfg["rf_devs"][args.name]
except KeyError:
	print("yaml error")


device = device(*a.values())
    
print(device)
rfdevice = RFDevice(GPIOS[device.freq])
rfdevice.enable_tx()
rfdevice.tx_repeat = device.repeats
rfdevice.tx_code(device.dec, device.protocol, device.pulse, device.length)
rfdevice.cleanup()



