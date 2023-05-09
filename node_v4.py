#going to update for3 nodes 
import time
from datetime import datetime
import ADS1x15
#import random
import json
import matplotlib.pyplot as plt
import numpy as np
from obspy import Trace, Stream, UTCDateTime
import socket
import sys

import paho.mqtt.client as mqtt

# IP address and port number of t	he PC
PC_IP = '192.168.8.112'
PC_PORT = 500
node_name = 'nodeRH'

# create a socket object
dplot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("waitting....")
dplot.connect((PC_IP, PC_PORT))
print("dplot is connected")


sample_rate =475
time_window =180

ADS = ADS1x15.ADS1113(1, 0x48)
ADS.setDataRate(ADS.DR_ADS111X_475) #data rate 860 samples per sec
# print(ADS.getDataRate())
ADS.setMode(ADS.MODE_CONTINUOUS)
ADS.requestADC(0)                   # First read to trigger


def reconnect():
    dplot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dplot.connect((PC_IP, PC_PORT))
def file_create(sample_set,rate,starting_time):
    trace = Trace(data= sample_set, header={"starttime": starting_time,"sampling_rate":rate})
    st1 = Stream(traces=[trace])
    na = '_'.join(str(starting_time).split(":"))
    name = node_name+'/'+node_name+'_signal'+na+".mseed"
    st1.write(name, format="MSEED")
count = 0
while True :

    sequence = np.array([])
    starting_time = datetime.now()
    print(datetime.now(),count)

    while(time_window*sample_rate>len(sequence)):

        start_time= datetime.now()
        raw = ADS.getValue()
        # Generate a random value between 0 and 3
        #vol = random.uniform(0, 3)
        vol=ADS.toVoltage(raw)
        sequence = np.append(sequence,[vol])
        t = datetime.now().timestamp()
        # json_data = json.dumps({f"{t:.6f}":f"{vol:.3f}"})+"+"
        try:
            dplot.sendall(bytes(f"{t:.6f}:"+f"{vol:.3f}"+"+",'utf-8'))
            # dplot.sendall(json_data.encode('utf-8'))
        except:
            pass
        end_time = datetime.now()
        delay=end_time-start_time
        interval= 2.1052e-3 -delay.total_seconds()
        
        if(interval>=0):           
            time.sleep(interval)
        else:
            continue
        
    file_create(sequence,sample_rate , starting_time)
    count+=1
s.close()
