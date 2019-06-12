import grovepi
import math
import paho.mqtt.client as mqtt
from datetime import datetime
import time

def on_connect(client, userdata, flags, rc):
    if rc==0:
       print("Connected")

mqttc = mqtt.Client("P1")
mqttc.on_connect = on_connect

sensor = 4
blue = 0
white = 1

# Connect
mqttc.username_pw_set('rnzmvzya', 'XwYSvlxWroVR')
mqttc.connect('m13.cloudmqtt.com',16433 )

while True:
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    try:
        [Temp,Hum] = grovepi.dht(sensor,blue)
        if math.isnan(Temp) == False and math.isnan(Hum) == False:
            print( "temp = %.02f C humidity = %.02f%%"%(Temp,Hum))
            mqttc.publish("temp",Temp)
            mqttc.publish("hum",Hum)
	    time.sleep(1)
    except:
        print ("Error while reading sensor data and sending to Gateway")
