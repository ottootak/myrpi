import os
import re
import threading
import time
from dataclasses import dataclass
from bluepy import btle
from db_commands import insert_temperature

adress = "A4:C1:38:2C:60:CE"
pid = os.getpid()
time_started = int(time.time())
time_unconnected = None
connected = False

@dataclass
class Measurement:
	temperature: float
	humidity: int
	voltage: float
	#timestamp: int       
	def list_data(self):
		return [self.temperature, self.humidity, self.voltage,
				self.timestamp]
        #metoda na __eq__
        
class MyDelegate(btle.DefaultDelegate):
	def __init__(self, params):
		btle.DefaultDelegate.__init__(self)
	
	def handleNotification(self, cHandle, data):
		try:
			measurement = Measurement(0,0,0)
			measurement.temperature = int.from_bytes(data[0:2], byteorder='little') / 100
			measurement.humidity = int.from_bytes(data[2:3], byteorder='little')
			measurement.voltage = int.from_bytes(data[3:5], byteorder='little') / 1000
			a = False
			print("data prectena")
			insert_temperature((measurement.temperature, measurement.humidity, measurement.voltage, "1"))
		except Exception as e:
			print("chyba v handlenotif")

def check_bluepid():
	pstree=os.popen("pstree -p " + str(pid)).read()
	bluepypid=0
	try:
		bluepypid=re.findall(r'bluepy-helper\((.*)\)',pstree)[0] #Store the bluepypid, to kill it later
	except IndexError: #Should normally occur because we're disconnected
		print("Couldn't find pid of bluepy-helper")
	if bluepypid != 0:
		os.system("kill " + bluepypid)
		print("Killed bluepy with pid: " + str(bluepypid))

def thread_watchDog ():
	while True:
		time_now = int(time.time())
		if((time_now - time_started) > 150):
			p.disconnect()
			time.sleep(3)
			check_bluepid()
			os._exit(-2)
		time.sleep(5)
    



thread_watchDog = threading.Thread(target=thread_watchDog)
thread_watchDog.start()
#watchdogthreadstarted


def connect():
	p = btle.Peripheral(adress)
	p.writeCharacteristic(0x0038,b'\x01\x00',True) #enable notifications of Temperature, Humidity and Battery voltage
	p.writeCharacteristic(0x0046,b'\xf4\x01\x00',True)
	p.withDelegate(MyDelegate("test"))
	return p
    
max_count = 1
count = 0
while True:
	try:
		if not connected:
			p = connect()
			connected = True
			
		if p.waitForNotifications(2000):
			count += 1
			if count >= max_count:
				connected = False
				p.disconnect()
				time.sleep(3)
				check_bluepid()
				os._exit(0)
	except Exception as e:
		print(e)
		connected = False
	print("waiting")






