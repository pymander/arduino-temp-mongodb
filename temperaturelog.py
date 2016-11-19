import serial
import time

# Configuration
serial_port = '/dev/ttyACM1'

#Connect to Serial Port for communication
ser = serial.Serial(serial_port, 9600, timeout=0)

#Setup a loop to send Temperature values at fixed intervals
#in seconds
fixed_interval = 10
while 1:
    try:
        # Temperature value obtained from Arduino + LM35 Temp Sensor
        temperature_c = ser.readline().rstrip()
        
        #Current time and date
        time_hhmmss = time.strftime("%H:%M:%S")
        date_mmddyyyy = time.strftime("%d/%m/%Y")

        #current location name
        temperature_location = "Mumbai-Kandivali"

        # If we received a measurement, print it and send it to MongoDB.
        if temperature_c:
            print temperature_c + ',' + time_hhmmss + ',' + date_mmddyyyy + ',' + temperature_location

        time.sleep(fixed_interval)
        
    except serial.SerialTimeoutException:
        print('Error! Could not read the Temperature Value from unit')
        time.sleep(fixed_interval)
