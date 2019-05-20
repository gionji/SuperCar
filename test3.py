import obd

#connection = obd.OBD() # auto connect

# OR

#connection = obd.OBD("/dev/ttyUSB0") # create connection with USB 0

# OR

ports = obd.scan_serial()      # return list of valid USB or RF ports
print ports                    # ['/dev/ttyUSB0', '/dev/ttyUSB1']

try:
	connection = obd.OBD(ports[0]) # connect to the first port in the list
	print(connection.status())
except Exception as e:
	connection = None
	print( e )


codes = [ 0x4, 0x5, 0x6, 0x7, 0x0c, 0x0d, 0x0e, 0x0f, 0x11, 0x21]

names = [
#'Supported PIDs [01-20]',
#'Status since DTCs cleared',
#'Fuel System Status',
'Calculated Engine Load',
'Engine Coolant Temperature',
'Short Term Fuel Trim - Bank 1',
'Long Term Fuel Trim - Bank 1',
#'Intake Manifold Pressure',
'Engine RPM',
'Vehicle Speed',
'Timing Advance',
'Intake Air Temp',
'Throttle Position',
#'O2 Sensors Present',
#'O2: Bank 1 - Sensor 1 Voltage',
#'O2: Bank 1 - Sensor 2 Voltage',
#'OBD Standards Compliance',
#'Supported PIDs [21-40]',
'Distance Traveled with MIL on',
]

for code, name in zip(codes, names):
	print str(name) + ": " + str(code)

while True:
	if connection is not None:
		if( connection.status() == obd.OBDStatus.CAR_CONNECTED ):
			for i, name in zip(codes, names):
				if (obd.commands.has_pid(1, i)):
					cmd = obd.commands[1][i]
					r = connection.query(cmd)
					print( str(name) + "  " +str(r) )
	
