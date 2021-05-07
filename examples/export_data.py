import sys, json, time

start_time = time.mktime(time.strptime('Fri May  7 23:42:58 2021'))


offset = None
with open(sys.argv[1], 'r') as infile:
	for line in infile:
		entry = json.loads(line)
		delta_ts = entry.pop('ts') * 1e-9

		if offset is None:
			offset = start_time - delta_ts
		
		ts = delta_ts + offset

		U, I = entry.pop('U'), entry.pop('I')
		P = U * I
		print(ts, U, I, P)