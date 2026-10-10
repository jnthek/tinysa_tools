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

f_low = 97.6e6
f_high = 97.8e6
N_points = 251
N_tstamps = 101
RBW = 6e3

wfall_buffer = np.zeros([N_tstamps,N_points])
freq, meas_power = get_tinysa_scan(f_low, f_high, N_points, RBW)

fig, [ax_spec, ax_wfall] = plt.subplots(2, 1, figsize=(16,9))
fig.canvas.manager.set_window_title('TinySA Spectrum Display tool') 
ax_wfall.axis('off')

im = ax_wfall.imshow(wfall_buffer, aspect='auto', cmap='rainbow', vmin=np.min(meas_power), vmax=np.max(meas_power))
line, = ax_spec.plot([], [], lw=1, color='red')

ax_spec.grid(True)
ax_spec.set_xlabel("Freq (MHz)")
ax_spec.set_ylabel("Power (dBm)")
set_lims = True

def animate_func(i):

    global wfall_buffer
    global set_lims
    wfall_buffer = np.roll(wfall_buffer, shift=1, axis=0)
    freq, meas_power = get_tinysa_scan(f_low, f_high, N_points, RBW)

    wfall_buffer[0,:] = meas_power
    im.set_array(wfall_buffer)
    line.set_data(freq/1e6, meas_power)
    if set_lims:
        ax_spec.set_xlim(min(freq/1e6),max(freq/1e6))
        ax_spec.set_ylim(min(meas_power)-10, max(meas_power)+10)
        set_lims = False

    return [im]

anim = animation.FuncAnimation(fig, animate_func, frames = None)
                               
plt.show() 

