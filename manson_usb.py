import enum, serial

class OPERATING_MODE(enum.Enum):
	CV = 0
	CC = 1

#This is an ugly hack to get readline to work with '\r' terminated lines.
#It also encodes and decodes for us.
class manson_serial(serial.Serial):
	def read(self, *pos):
		return super().read(*pos).replace(b'\r', b'\n')

	def readline(self):
		return str(super().readline(), 'ascii')

	def writeline(self, line):
		super().write(bytes(line, 'ascii') + b'\r')

class instrument_interface:
	def __init__(self, port):
		self.port = port

	def _query_lines(self, query, num_lines):
		self.port.writeline(query)
		lines = [self.port.readline() for i in range(num_lines + 1)]
		ok_line = lines.pop(-1)
		assert ok_line == 'OK\n' and len(lines) == num_lines
		return lines

	def _test_query(self, query):
		'This will read lines until timeout is hit - only use for testing purposes'
		self.port.writeline(query)
		lines = self.port.readlines()
		return lines

	def _query_single_line(self, query):
		return self._query_lines(query, 1)[0].rstrip('\n')

	def _execute_command(self, command):
		self._query_lines(command, 0)

	@staticmethod
	def _parse_deci_voltage_current_line(line):
		assert len(line) == 6
		decivolts = int(line[:3])
		deciamperes = int(line[3:])
		return decivolts * .1, deciamperes * .1

	def get_model(self):
		return self._query_single_line('GMOD')

	def get_maximums(self):
		'Returns a tuple of maximum voltage and current'
		return self._parse_deci_voltage_current_line(self._query_single_line('GMAX'))

	def get_measurement(self):
		'Returns current measurements of voltage, current and operating mode'
		answer = self._query_single_line('GETD')
		assert len(answer) == 9
		centivolts = int(answer[:4])
		centiamperes = int(answer[4:8])
		mode = OPERATING_MODE(int(answer[8:9]))
		return centivolts * .01, centiamperes * .01, mode

	def get_preset(self):
		'Returns set voltage and current limit'
		return self._parse_deci_voltage_current_line(self._query_single_line('GETS'))

	def get_memory(self):
		data = self._query_single_line('GETM')
		result = list()
		while data:
			line, data = data[:6], data[6:]
			result.append(self._parse_deci_voltage_current_line(line))

		return result

	def set_memory(self, *voltage_current_pairs):
		data = ''
		for voltage, current in voltage_current_pairs:
			decivolts = int(voltage * 10)
			deciamperes = int(current * 10)
			data += f'{decivolts:03d}{deciamperes:03d}'
		self._execute_command(f'PROM{data}')

	def set_enable(self, state):
		self._execute_command(f'SOUT{0 if state else 1}')	#Note that 0 means enabled

	def set_current_limit(self, current):
		deciamperes = int(current * 10)
		self._execute_command(f'CURR{deciamperes:03d}')

	def set_voltage(self, voltage):
		decivolts = int(voltage * 10)
		self._execute_command(f'VOLT{decivolts:03d}')

	def run_memory(self, index):
		self._execute_command(f'RUNM{index}')
