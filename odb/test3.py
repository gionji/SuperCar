import obd
import sys
import time
import detetime

#connection = obd.OBD() # auto connect
# OR
#connection = obd.OBD("/dev/ttyUSB0") # create connection with USB 0


MODE = 1

COMMANDS = [
	(0x00, 'Supported PIDs [01-20]'       , 'PIDS_A' ),
	(0x01, 'Status since DTCs cleared'    , 'STATUS' ),
	(0x03, 'Fuel System Status'           , 'FUEL_STATUS' ),
	(0x04, 'Calculated Engine Load'       , 'ENGINE_LOAD' ),
	(0x05, 'Engine Coolant Temperature'   , 'COOLANT_TEMP' ),
	(0x06, 'Short Term Fuel Trim - Bank 1', 'SHORT_FUEL_TRIM_1' ),
	(0x07, 'Long Term Fuel Trim - Bank 1' , 'LONG_FUEL_TRIM_1' ),
	(0x0b, 'Intake Manifold Pressure'     , 'INTAKE_PRESSURE' ),
	(0x0c, 'Engine RPM'                   , 'RPM' ),
	(0x0d, 'Vehicle Speed'                , 'SPEED' ),
	(0x0e, 'Timing Advance'               , 'TIMING_ADVANCE' ),
	(0x0f, 'Intake Air Temp'              , 'INTAKE_TEMP' ),
	(0x11, 'Throttle Position'            , 'THROTTLE_POS' ),
	(0x13, 'O2 Sensors Present'           , 'O2_SENSORS' ),
	(0x14, 'O2: Bank 1 - Sensor 1 Voltage', 'O2_B1S1' ),
	(0x15, 'O2: Bank 1 - Sensor 2 Voltage', 'O2_B1S2' ),
	(0x1c, 'OBD Standards Compliance'     , 'OBD_COMPLIANCE' ),
	(0x20, 'Supported PIDs [21-40]'       , 'PIDS_B' ),
	(0x21, 'Distance Traveled with MIL on', 'DISTANCE_W_MIL' )
]



def saveData(filename, data):
	with open(filename,  "a") as myfile:
		myfile.write( str(data) )



def main():

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
		if connection is not None:
			if( obd.is_connected() ):
				values = list()
				for cmd in commands:
					response = connection.query(odb.command[cmd])
					values.append( [cmd, response] )

				time.sleep(1.0
				print( values )
				saveData('civic.log', str(values) )

if __name__ == "__main__":
	main()
