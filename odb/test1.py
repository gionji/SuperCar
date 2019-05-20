import obd

#connection = obd.OBD() # auto connect

# OR

#connection = obd.OBD("/dev/ttyUSB0") # create connection with USB 0

# OR

ports = obd.scan_serial()      # return list of valid USB or RF ports
print ports                    # ['/dev/ttyUSB0', '/dev/ttyUSB1']

connection = obd.OBD(ports[0]) # connect to the first port in the list

print connection.status()


if( connection.status() == obd.OBDStatus.CAR_CONNECTED ):
	for i in range(0,0x5e):
		if (obd.commands.has_pid(1, i)):
			cmd = obd.commands[1][i]
			r = connection.query(cmd)
			print( str(r) )
	
