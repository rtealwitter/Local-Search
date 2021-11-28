filename = 'data/temperature.txt'
# Sensors with more than 10,000 observations with temps within recorded temps of Berkeley, CA
# [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]
COMMON_SENSORS = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]
NUM_COMMON = len(COMMON_SENSORS)
observations = {}

with open(filename, 'r') as f:
    for line in f.readlines():
        vals = line.split()
        if len(vals) >= 5: 
            sensor_id, temp = int(vals[3]), float(vals[4])
            time = vals[0] + '/' + vals[1][:5]
            # Within range of recorded temperature in Berkeley, CA
            if -4 <= temp and temp <= 42 and sensor_id in COMMON_SENSORS:
                if time not in observations:
                    observations[time] = ['NA']*NUM_COMMON
                observations[time][COMMON_SENSORS.index(sensor_id)] = temp


num_all = 0
for time in observations:
    if observations[time].count('NA') == 0:
        print(observations[time])
        num_all += 1

print(len(COMMON_SENSORS))
print(num_all)
