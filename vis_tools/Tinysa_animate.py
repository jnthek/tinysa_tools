import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from pylab import *
import serial
from time import sleep

def get_tinysa_scan(f_low, f_high, N_points, RBW):
    ser = serial.Serial(port='/dev/cu.usbmodem4001', baudrate=115200)
    ser.timeout = 0.05
    rbw_command = "rbw "+str(int(RBW/1e3))
    scan_command = "scan"+" "+str(int(f_low))+" "+str(int(f_high))+" "+str(int(N_points))+" 3"
    result = ""
    data = ""
    ser.write(str(rbw_command + "\r").encode('ascii'))
    sleep(0.05)
    ser.write(str(scan_command + "\r").encode('ascii'))  
    sleep(0.05)
    while data != "ch> ":
        data = ser.readline().decode('ascii')
        result += data
    values = result.split("\r\n")
    ser.close() 

    m_power = np.zeros(len(values)-3)
    m_freq = np.zeros(len(values)-3)

    for i in range(len(values)-3):
        m_freq[i] = float(values[i+2].split(" ")[0])
        m_power[i] = float(values[i+2].split(" ")[1])
    return m_freq, m_power

fig = plt.figure(figsize=(16,9))
ax = plt.axes(ylim=(-100, -50))
line, = ax.plot([], [], lw=1, color='red')
ax.grid()
ax.set_xlabel("Freq (MHz)")
ax.set_ylabel("Power (dBm)")
set_lims = True
def animate(i, f_low, f_high, N_points, RBW_here):	
	global set_lims
	freq, meas_power = get_tinysa_scan(f_low, f_high, N_points, RBW_here)
	
	if set_lims:
		ax.set_xlim(min(freq/1e6), max(freq/1e6))
		ax.set_ylim(min(meas_power)-10, max(meas_power)+10)
		set_lims = False
	line.set_data(freq/1e6, meas_power)
	return line,
	
anim = animation.FuncAnimation(fig=fig, func=animate, fargs=[50e6, 250e6, 250, 600e3], frames=None)
plt.show()