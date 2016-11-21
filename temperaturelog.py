import serial
import time
import datetime
from pymongo import MongoClient

# Configuration
serial_port          = '/dev/ttyACM0'
mongodb_host         = '70.42.161.213'
mongodb_db           = 'temperature'
temperature_location = "Mumbai-Kandivali"

# Connect to Serial Port for communication
ser = serial.Serial(serial_port, 9600, timeout=0)

# Connect to MongoDB
client = MongoClient(mongodb_host, 27017)
db = client[mongodb_db]
collection = db['templog']

# Setup a loop to send Temperature values at fixed intervals in seconds
fixed_interval = 10
while 1:
    try:
        # Temperature value obtained from Arduino + LM35 Temp Sensor
        temp_string = ser.readline().rstrip()
        
        # If we received a measurement, print it and send it to MongoDB.
        if temp_string:
            temperature_c = float(temp_string)
            doc_id = collection.insert_one({ 'temperature': temperature_c,
                                             'datetime': datetime.datetime.now(),
                                             'location': temperature_location}).inserted_id
            print str(doc_id) + ': ' + str(temperature_c) + ',' + temperature_location
    except serial.SerialTimeoutException:
        print('Error! Could not read the Temperature Value from unit')
    except ValueError:
        print('Error! Could not convert temperature to float')
    finally:
        time.sleep(fixed_interval)
