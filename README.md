# DHT22-Spike-Check

Simple Python script to monitor tempertures in Garage. Output is to a .txt file for use by Weewx
Initial issue was an occasional spike in Humidity to 1000 - 3000%.  
Seems noise related and I continue to seek out the source.  

In the mean time this script sets the Temp to 100C if it sees a Humidity Spike and then reruns the sensor querry.

 
