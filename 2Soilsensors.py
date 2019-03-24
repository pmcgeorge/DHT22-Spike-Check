import subprocess
import glob
import time
from datetime import datetime

sensor1 = '28-0113170101b8'# you need to add each sensor's address manually to these lines
sensor2 = '28-0113170a5ceb'# you need to add each sensor's address manually to these lines
sensor1name = '6-inch'
sensor2name = '4-inch'


base_dir1 = '/sys/bus/w1/devices/'
device_folder1 = glob.glob(base_dir1 + sensor1)[0] 
device_file1 = device_folder1 + '/w1_slave'

def read_temp_raw1():
        catdata = subprocess.Popen(['cat',device_file1], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = catdata.communicate()
        out_decode = out.decode('utf-8')
        lines = out_decode.split('\n')
        return lines

def read_temp1():
        lines = read_temp_raw1()
        while lines[0].strip()[-3:] != 'YES':
                time.sleep(10.0)
                lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                return temp_f

base_dir2 = '/sys/bus/w1/devices/'
device_folder2 = glob.glob(base_dir2 + sensor2)[0] 
device_file2 = device_folder2 + '/w1_slave'

def read_temp_raw2():
        catdata = subprocess.Popen(['cat',device_file2], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = catdata.communicate()
        out_decode = out.decode('utf-8')
        lines = out_decode.split('\n')
        return lines

def read_temp2():
        lines = read_temp_raw2()
        while lines[0].strip()[-3:] != 'YES':
                time.sleep(10.0)
                lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                return temp_f


while True:
    
    date = datetime.today().strftime("%x , %X")
    temp1 = str(read_temp1())
    temp2 = str(read_temp2())
    print (sensor1name+' = '+temp1)
    print (sensor2name+' = '+temp2)
    fd = open('/home/pi/soiltemp.txt','w')
    fd.write(sensor1name+' = '+temp1+'\n')
    fd.write(sensor2name+' = '+temp2+'\n')
    fd.close()
    
    
    

    time.sleep(25.0)
