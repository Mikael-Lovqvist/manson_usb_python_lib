from manson_usb import manson_serial, instrument_interface
import time, json

with manson_serial('/dev/ttyUSB0', baudrate=9600, timeout=0.1) as port:
	instrument = instrument_interface(port)

	while True:
		voltage, current, mode = instrument.get_measurement()
		time.sleep(1)
		print(json.dumps(dict(ts=time.monotonic_ns(), U=voltage, I=current, m=mode.name)))
