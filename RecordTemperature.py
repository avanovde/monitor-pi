from datetime import datetime
import time
import os


def temp_raw(sensor):
  sensor_file = device_path + "/" + sensor + "/" + w1_slave
  f = open(sensor_file, 'r')
  lines = f.readlines()
  f.close()
  return lines


def read_temp(sensor):
  lines = temp_raw(sensor)
  while lines[0].strip()[-3] != 'YES':
      time.sleep(0.2)
      lines = temp_raw(sensor)
      temp_output = lines[1].find('t=')

      if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f


# Configuration
sensors = ['28-0417c3aeb9ff']
log_file_path = '/var/log/temperature/'


# Load drivers
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

device_path = '/sys/bus/w1/devices'
w1_slave = 'w1_slave'

# Bulid up a new log file entry
now = datetime.now()
entry = str(now)
for sensor in sensors:
  entry += "," + str(read_temp(sensor))
entry += "\n"

# Write the temperature and timestamp out to the log
# There will be a log file for each month
log_file = log_file_path + str(now.year) + "-" + str(now.month) + ".csv"
log_file_stream = open(log_file, 'a')
log_file_stream.write(entry)

# crontab -e /5 * * * * python /path/to/script