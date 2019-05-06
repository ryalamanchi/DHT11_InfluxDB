import RPi.GPIO as GPIO
import dht11
import time
import datetime
from influxdb import InfluxDBClient

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# initialize influxDB
host=input("Enter host IP address where InfluxDB is running:");
port = "8086"
dbname = "mysensordb"
interval = 1

#Measurement details
measurement = "dht11-beadroom"
location = "home"


# read data using pin 14
instance = dht11.DHT11(pin=4)

# create InfluxDB client object
client = InfluxDBClient(host=host, port=port, database=dbname)
try:
    while True:
        result = instance.read()
        temperature = result.temperature
        humidity = result.humidity
        iso_time = time.ctime()
        data = [
        {
            "measurement": measurement,
            "tags": {
                "location": location,
            },
            "fields": {
                "temperature": temperature,
                "humidity": humidity
            }
        }
        ]
        if result.is_valid():
            client.write_points(data)
            #print("Last valid input: " + str(datetime.datetime.now()))
            print("Last valid input: " + iso_time)
            print("Temperature: %d C" % result.temperature)
            print("Humidity: %d %%" % result.humidity)

        time.sleep(interval)
except KeyboardInterrupt:
    pass
