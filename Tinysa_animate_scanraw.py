import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from pylab import *
import serial
from time import sleep
from struct import *

def get_tinysa_scanraw(f_low, f_high, N_points, RBW):
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
    ser.timeout = 100
    ser.flushInput()
    ser.flushOutput()
    ser.flush()
    ser.read_all()
    rbw_command = "rbw "+str(int(RBW/1e3))
    scan_command = "scanraw"+" "+str(int(f_low))+" "+str(int(f_high))+" "+str(int(N_points))
    result = ""
    data = ""
    ser.write(str(rbw_command + "\r").encode('ascii'))
    sleep(0.05)
    ser.write(str(scan_command + "\r").encode('ascii'))  
    sleep(0.05)
    ser.readline()
    ser.readline()
    bin_data = ser.read_until(b"}ch> ")
    read_data = unpack('cBB'*N_points,bin_data[1:-5])
    m_power = np.zeros(N_points, dtype=np.float64)
    for i in range(N_points):
        m_power[i] = (read_data[i*3+1] + read_data[i*3+2]*256)/32-128
    ser.close() 
    return m_power

fig = plt.figure(figsize=(16,9))
ax = plt.axes(ylim=(-100, -50))
line, = ax.plot([], [], lw=1, color='red')
ax.grid()
ax.set_xlabel("Freq (MHz)")
ax.set_ylabel("Power (dBm)")
set_lims = True
def animate(i, f_low, f_high, N_points, RBW_here):	
    global set_lims
    freq = np.linspace(f_low, f_high, N_points)
    meas_power = get_tinysa_scanraw(f_low, f_high, N_points, RBW_here)
    if set_lims:
        ax.set_xlim(min(freq/1e6), max(freq/1e6))
        ax.set_ylim(min(meas_power)-10, max(meas_power)+10)
        set_lims = False
    line.set_data(freq/1e6, meas_power)
    return line,
	
anim = animation.FuncAnimation(fig=fig, func=animate, fargs=[50e6, 250e6, 2000, 100e3], frames=None)
plt.show()