import time
import Adafruit_DHT
import io
import paho.mqtt.client as mqtt

sensor = Adafruit_DHT.DHT22
pin = 23

#MQTT Settings
mqtt_server = "BROKER_IP"
mqtt_port = 1883
mqtt_topic1 = "sensors/garage/Gtemp"
mqtt_topic2 = "sensors/garage/Ghumid"
Interval = 20

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("MQTT connected OK")
    else:
        print("Bad connection Returned code=",rc)

mqtt.Client.connected_flag=False#create flag in class

next_reading = time.time()
client = mqtt.Client('garagepi')

client.loop_start()
client.on_connect = on_connect
client.connect(mqtt_server,mqtt_port,60)

while not client.connected_flag: #wait in loop
    print("In wait loop")
    time.sleep(1)

try:
    while True:
        temperature = 100
        while temperature == 100:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

            if humidity > 1000:
                temperature = 100
                time.sleep(1)


# Un-comment the line below to convert the temperature to Fahrenheit.
        Temp = '{:.2f}'.format(9.0 / 5.0 * temperature + 32)


        humidity = '{:.2f}'.format(humidity)

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!

        if humidity is not None and Temp is not None:

            client.publish(mqtt_topic1,Temp);
            #needs a pause or it misses humidity
            #time.sleep(.2)
            #publish humidity
            client.publish(mqtt_topic2,humidity);
            next_reading += Interval
            sleep_time = next_reading-time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)

        else:
            fd = open('/home/pi/SensorData/DHTsensor.txt','a')
            fd.write(time.strftime("%H:%M:%S\n"))
            fd.write('Failed to get reading. Try again!')
            fd.close()

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
