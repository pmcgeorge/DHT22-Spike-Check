import time
import Adafruit_DHT
import io

sensor = Adafruit_DHT.DHT22
pin = 23

cpt = open("/sys/class/thermal/thermal_zone0/temp", 'r')
cpuT = float(cpt.readline ())
cputemp = cpuT/1000 * 1.8 + 32


while True:
    temperature = 100
    while temperature == 100:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        
        if humidity > 200 or humidity < 0 or temperature > 50 or temperature < -25:
            temperature = 100
        
        
        print ('Humidity={0:0.1f}%'.format(humidity))
        time.sleep(1)


# Un-comment the line below to convert the temperature to Fahrenheit.
    Temp = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!

#   print (time.strftime("%H:%M:%S"))
#   print "cputemp = %sF" %(cputemp)

    if humidity is not None and temperature is not None:

        print('Temp={0:0.1f}*F Humidity={1:0.1f}%'.format(Temp, humidity))

    # fd = open('/home/pi/SensorData/DHTsensor.txt','w')
    # fd.write(time.strftime("%H:%M:%S "))
    # fd.write('GarageTemp = {0:0.1f}\nGarageHumidity = {1:0.1f}\n'.format(Temp, humidity))
    # fd.write ("CPUTemp = %s\n" %(cputemp))
    # fd.write ("CPUTemp C = %s\n" %(cpuT/1000))
    # fd.close()


    else:
        fd = open('/home/pi/SensorData/DHTsensor.txt','a')
        #fd.write(time.strftime("%H:%M:%S\n"))
        fd.write('Failed to get reading. Try again!')
        fd.close()
    
    time.sleep(5)

