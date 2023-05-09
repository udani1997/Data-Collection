#going to update for3 nodes 
import time
from datetime import datetime
import ADS1x15
#import random


import matplotlib.pyplot as plt
import numpy as np
from obspy import Trace, Stream, UTCDateTime
import socket
import sys


# IP address and port number of t	he PC
PC_IP = '192.168.8.112'
PC_PORT = 500
node_name = 'NodeRH'

# create a socket object
print("waiting....")
dplot = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("dplot is connected")


sample_rate =475
time_window =60

ADS = ADS1x15.ADS1113(1, 0x48)
ADS.setDataRate(ADS.DR_ADS111X_475) #data rate 860 samples per sec
# print(ADS.getDataRate())
ADS.setMode(ADS.MODE_CONTINUOUS)
ADS.requestADC(0)                   # First read to trigger



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
    v=0
    while(time_window*sample_rate>len(sequence)):
        #sys.stdout.write("\rCurrent time: " + str(datetime.now()))
        #sys.stdout.flush()
        #print("\rCurrent time:", current_time, end="")
        start_time= datetime.now()
        raw = ADS.getValue()
        # Generate a random value between 0 and 3
        #vol = random.uniform(0, 3)
        vol=ADS.toVoltage(raw)
        sequence = np.append(sequence,[vol])
        t = datetime.now().timestamp()
        dplot.sendto((f"{t}:"+f"{vol:.3f}:"+f"{v:05}+").encode(),(PC_IP,PC_PORT))
        end_time = datetime.now()
        delay=end_time-start_time
        interval= 2.10526315e-3 -delay.total_seconds()
        v+=1
        if(interval>=0):
            time.sleep(interval)
        else:
            continue
    file_create(sequence,sample_rate , starting_time)
    print(len(sequence),v)
    count+=1
s.close()