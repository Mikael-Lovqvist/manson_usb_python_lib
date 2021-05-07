import sys, json, time

ts = None
total_energy = 0
with open(sys.argv[1], 'r') as infile:
	for line in infile:
		entry = json.loads(line)
		previous_ts = ts
		ts = entry.pop('ts') * 1e-9

		U, I = entry.pop('U'), entry.pop('I')
		power = U * I

		if previous_ts is not None:
			previous_power = power
			delta_ts = ts - previous_ts

			delta_power = abs(previous_power - power)
			common_power = min(abs(previous_power), abs(power))
			energy = (common_power + delta_power) * delta_ts	#watt seconds or joules
			total_energy += energy


def joules_to_wh(E):
	return E / 3600

print(f'Total energy: {total_energy*1e-3:.2f} kJ ({joules_to_wh(total_energy):.2f} Wh)')