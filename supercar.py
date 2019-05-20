import obd
import sys
import time
import detetime

from os import system, devnull
from subprocess import call, STDOUT
from sys import exit
from time import sleep
from threading import Thread


class Accel:
	def __init__(self):
		self.accel = [0, 0, 0]
		self.calib = [0, 0, 0]
		self.valSub = []
		self.raw = ""
		try:
			with open("/sys/class/misc/FreescaleAccelerometer/enable", "w") as enabler:
				enabler.write("1")
		except:
			print "Error: No Accel detected"

	def calibrate(self):
		self.valSub = self.get()
		for num in range(0, len(self.accel)):
			self.calib[num] = self.valSub[num]
		sleep(0.5)
		for num in range(0, len(self.accel)):
			self.calib[num] = self.valSub[num]

	def get(self):  # Return accel data in array
		try:
			with open("/sys/class/misc/FreescaleAccelerometer/data", "r") as reader:
				self.raw = str(reader.read().replace('\n', ''))
			for a in range(0, 3):
				try:
					self.accel[a] = (int(self.raw[0:self.raw.index(',')]) if ',' in self.raw else int(self.raw))
					self.raw = self.raw[self.raw.index(',') + 1:]
				except:
					break
		except:
			print "Error using accelerometer!"
		finally:
			for num in range(0, len(self.accel)):
				self.accel[num] -= self.calib[num]
			return self.accel  # return like this [x, y, z] in integer formats


class Magno:
	def __init__(self):
		self.magn = [0, 0, 0]
		self.calib = [0, 0, 0]
		self.valSub = []
		self.raw = ""
		try:
			with open("/sys/class/misc/FreescaleMagnetometer/enable", "w") as enabler:
				enabler.write("1")
		except:
			print "Error: No Magnometer detected"

	def calibrate(self):
		self.valSub = self.get()
		for num in range(0, len(self.magn)):
			self.calib[num] = self.valSub[num]
		sleep(0.5)
		for num in range(0, len(self.magn)):
			self.calib[num] = self.valSub[num]

	def get(self):  # Return mango data in array
		with open("/sys/class/misc/FreescaleMagnetometer/data", "r") as reader:
			self.raw = str(reader.read().replace('\n', ''))
		for a in range(0, 3):
			try:
				self.magn[a] = (int(self.raw[0:self.raw.index(',')]) if ',' in self.raw else int(self.raw))
				self.raw = self.raw[self.raw.index(',') + 1:]
			except:
				break
		for num in range(0, len(self.magn)):
			self.magn[num] -= self.calib[num]
		return self.magn  # return like this [x, y, z] in integer formats


class Gyro:
	def __init__(self):
		self.gyro = [0, 0, 0]
		self.calib = [0, 0, 0]
		self.valSub = []
		self.raw = ""
		try:
			with open("/sys/class/misc/FreescaleGyroscope/enable", "w") as enabler:
				enabler.write("1")
		except:
			print "Error: No Gyro detected"

	def calibrate(self):
		self.valSub = self.get()
		for num in range(0, len(self.gyro)):
			self.calib[num] = self.valSub[num]
		sleep(0.5)
		for num in range(0, len(self.gyro)):
			self.calib[num] = self.valSub[num]

	def get(self):  # Return gyro data in array
		with open("/sys/class/misc/FreescaleGyroscope/data", "r") as reader:
			self.raw = str(reader.read().replace('\n', ''))
		for a in range(0, 3):
			try:
				self.gyro[a] = (int(self.raw[0:self.raw.index(',')]) if ',' in self.raw else int(self.raw))
				self.raw = self.raw[self.raw.index(',') + 1:]
			except:
				break
		for num in range(0, len(self.gyro)):
			self.gyro[num] -= self.calib[num]
		return self.gyro  # return like this [x, y, z] in integer formats


MODE = 1


def saveData(filename, data):
	with open(filename,  "a") as myfile:
		myfile.write( str(data) )


def main():

	gyro = Gyro() # new objects p.s. this will auto initialize the device onboard
	accel = Accel()
	magno = Magno()

	accel.calibrate()
	gyro.calibrate() # Reset current values to 0
	magno.calibrate()

	commands = [
				'ENGINE_LOAD',
				'RPM',
				'SPEED',
				'SHORT_FUEL_TRIM_1',
				'LONG_FUEL_TRIM_1',
				'THROTTLE_POS',
				'DISTANCE_W_MIL'
				 ]

	connection = None

	ports = obd.scan_serial()

	if len(ports) > 0:
		print('Available ports:')
		print(ports)

	try:
		connection = obd.OBD( port ) # connect to the first port in the list
		print( connection.status() )
	except Exception as e:
		connection = None

	while True:

		values = list()

		acc = accel.get() # Same as gyro return xyz of current displacment force
		mag = magno.get() # 
		gyr = gyro.get() # Returns a full xyz list [x,y,z] realtime (integers/degrees)


		values.append(['accX', str(acc[0])])
		values.append(['accY', str(acc[1])])
		values.append(['accZ', str(acc[2])])

		if connection is not None:
			if( obd.is_connected() ):
				for cmd in commands:
					response = connection.query(odb.command[cmd])
					values.append( [cmd, response] )

				time.sleep(1.0
				print( values )
				saveData('civic.log', str(values) )

if __name__ == "__main__":
	main()
