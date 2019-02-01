import argparse
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
import datetime
import time
import random
import paho.mqtt.client as mqtt
import psutil
import re


USER = 'root'
PASSWORD = 'root'
DBNAME = 'mydb1'
HOST = 'localhost'
PORT = 8086
dbclient = None;

mqtt_broker = "m2m.eclipse.org"
topic_sensor = "sensor"


my_mqtt = None

data1 = 0.0;
data2 = 0.0;
#Global variable to store Tempreture and Humidity

def main():
	startMQTT()
	dbclient = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)
	while True:
		data_point = getSensorData()
		dbclient.write_points(data_point)#write into database
		print(data_point)#show in terminal
		time.sleep(2)

def onMessage(client, userdata, message):
	
	message.payload = message.payload.decode("utf-8") #to remove the b infront
	str = message.payload
	ledata = re.findall(r"[-+]?\d*\.\d+|\d+", str)
	#seperate the numbers and put them into a list
	print(ledata)
	ledata1 = float(ledata[0])
	ledata2 = float(ledata[1])
	global data1
	data1 = ledata1
	global data2
	data2 = ledata2
	#store them to global variable
def startMQTT():
	my_mqtt = mqtt.Client()
	my_mqtt.on_message = onMessage
	my_mqtt.connect(mqtt_broker, port=1883)
	my_mqtt.subscribe(topic_sensor,qos =1 )
	my_mqtt.loop_start()
	print("subscribed to topic")


def getSensorData():
	
	now = time.gmtime()
	pointValues = [
		{
			"time": time.strftime("%Y-%m-%d %H:%M:%S", now),
			"measurement": 'reading',
			"tags": {
				"nodeId": "node_1",
			},
			"fields": {
				"Tempreture": data1,
				"Humidity": data2
				
			},
		}
	]

	return(pointValues)

if  __name__ == '__main__':
	main()
