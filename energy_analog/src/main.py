import serial
import time
from data import valid_data, invalid_data_0, invalid_data_1, invalid_data_2
import sys
import random

invalid_data = [
    invalid_data_0,
    invalid_data_1,
    invalid_data_2
]

l1_current = 0
l2_current = 0
l3_current = 0
l1_voltage = 0
l2_voltage = 0
l3_voltage = 0
l1_active_power_out = 0
l2_active_power_out = 0
l3_active_power_out = 0
l1_active_energy_out = 2516
l2_active_energy_out = 3452
l3_active_energy_out = 2345
active_energy_out = l1_active_energy_out + l2_active_energy_out + l3_active_energy_out
time_last = 0

def send_valid_data(ser):
    global time_last
    global l1_current
    global l2_current
    global l3_current
    global l1_voltage
    global l2_voltage
    global l3_voltage
    global l1_active_power_out
    global l2_active_power_out
    global l3_active_power_out
    global l1_active_energy_out
    global l2_active_energy_out
    global l3_active_energy_out
    global active_energy_out

    time_ds = time.time() - time_last
    time_last = time.time()

    l1_current = 3 + (random.random() - 0.5)
    l2_current = 3 + (random.random() - 0.5)
    l3_current = 3 + (random.random() - 0.5)

    l1_voltage = 230 + (random.random() - 0.5)
    l2_voltage = 230 + (random.random() - 0.5)
    l3_voltage = 230 + (random.random() - 0.5)

    l1_active_power_out = (l1_current * l1_voltage)/1000
    l2_active_power_out = (l2_current * l2_voltage)/1000
    l3_active_power_out = (l3_current * l3_voltage)/1000
    
    l1_active_energy_out = l1_active_energy_out + l1_active_power_out * time_ds/3600
    l2_active_energy_out = l2_active_energy_out + l2_active_power_out * time_ds/3600
    l3_active_energy_out = l3_active_energy_out + l3_active_power_out * time_ds/3600

    active_power_out = l1_active_power_out + l2_active_power_out + l3_active_power_out
    active_energy_out = l1_active_energy_out + l2_active_energy_out + l3_active_energy_out

    ser.write(valid_data.format(
        active_energy_out=active_energy_out,
        active_energy_in=0,
        reactive_energy_out=0,
        reactive_energy_in=0,
        active_power_in=0,
        active_power_out=active_power_out,
        reactive_power_in=0,
        reactive_power_out=0,
        l1_active_energy_out=l1_active_energy_out,
        l1_active_energy_in=0,
        l1_reactive_energy_in=0,
        l1_reactive_energy_out=0,
        l1_active_power_in=0,
        l1_reactive_power_in=0,
        l2_active_energy_out=l2_active_energy_out,
        l2_active_energy_in=0,
        l2_reactive_energy_in=0,
        l2_reactive_energy_out=0,
        l2_active_power_in=0,
        l2_reactive_power_in=0,
        l3_active_energy_out=l3_active_energy_out,
        l3_active_energy_in=0,
        l3_reactive_energy_in=0,
        l3_reactive_energy_out=0,
        l3_active_power_in=0,
        l3_reactive_power_in=0,
        l1_voltage=l1_voltage,
        l1_current=l1_current,
        l2_voltage=l2_voltage,
        l2_current=l2_current,
        l3_voltage=l3_voltage,
        l3_current=l3_current
    ))
    print("Writing valid data")


def send_invalid_data(ser, i):
    ser.write(invalid_data[i])
    print("Writing invalid data")



if __name__ == "__main__":
    device = "/dev/ttyAMA0"
    if len(sys.argv) > 1:
        device = sys.argv[1]
    
    print("Using device", device)
        
    ser = serial.Serial ("/dev/ttyAMA0", 115200)

    while True:
        for i in range(0, 10):
            send_valid_data(ser)
            time.sleep(10)
        
        # for i in range(0, 10):
        #     send_invalid_data(ser, i % 3)
        #     time.sleep(10)
        
        # for i in range(0, 100):
        #     send_valid_data(ser)
        #     time.sleep(0.1)
        
        # for i in range(0, 100):
        #     send_invalid_data(ser, i % 3)
        #     time.sleep(0.1)
        
    