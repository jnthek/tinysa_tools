import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from pylab import *
import serial
from time import sleep
from struct import *
import argparse

def get_tinysa_scanraw(s_port, f_low, f_high, N_points, RBW):
    ser = serial.Serial(port=s_port, baudrate=115200)
    ser.timeout = 100 #Large timeout to enable high N sweeps, extremely buggy !
    ser.flushInput()
    ser.flushOutput()
    ser.flush()
    ser.read_all() #Trying everything to keep the serial buffer clean

    rbw_command = "rbw "+str(int(RBW/1e3))
    scan_command = "scanraw"+" "+str(int(f_low))+" "+str(int(f_high))+" "+str(int(N_points))
    attenuate_command = "attenuate "+str(0)

    ser.write(str(attenuate_command + "\r").encode('ascii')) 
    sleep(0.05)
    ser.readline() 
    ser.write(str(rbw_command + "\r").encode('ascii'))
    sleep(0.05)
    ser.readline() # To get rid of the rbw and scanraw ASCII outputs, I don't know why I need this
    ser.write(str(scan_command + "\r").encode('ascii'))  
    sleep(0.05)
    ser.readline() 
    sleep(0.05)

    bin_data = ser.read_until(b"}ch> ")
    read_data = unpack('cBB'*N_points,bin_data[1:-5])
    m_power = np.zeros(N_points, dtype=np.float64)
    for i in range(N_points):
        m_power[i] = (read_data[i*3+1] + read_data[i*3+2]*256)/32-128
    ser.close() 
    return m_power

parser = argparse.ArgumentParser(description='A simple TinySA Spectrum Display tool, written by VK6JN/VU3VWB')
parser.add_argument('-s', metavar='serial_port', help='Serial port name, for example /dev/cu.usbmodem4001 in Mac')
parser.add_argument('-f', metavar='frequency', help='Frequency in Hz format is f_low:f_high:RBW, for example 87e6:108e6:100e3')
parser.add_argument('-N', metavar='N_pnts', type=int, help='Number of spectral points to sweep')
parser.add_argument('-T', metavar='N_ts', type=int, help='Depth of the waterfall, i.e. number of timestamps. 100 is a reasonable number')
args = parser.parse_args()

s_port = str(args.s)

f_string = str(args.f).split(":")
f_low = float(f_string[0])
f_high = float(f_string[1])
RBW = float(f_string[2])

N_points = int(args.N)
N_tstamps = int(args.T)

wfall_buffer = np.zeros([N_tstamps,N_points])
freq = np.linspace(f_low, f_high, N_points)
meas_power = get_tinysa_scanraw(s_port, f_low, f_high, N_points, RBW)

fig, [ax_spec, ax_wfall] = plt.subplots(2, 1, figsize=(16,9))
fig.suptitle("Freq low : {:.2f} MHz".format(f_low/1e6)+", Freq high : {:.2f} MHz".format(f_high/1e6)+ \
                ", RBW : {:.2f} kHz".format(RBW/1e3)+", Npoints : {:.0f}".format(N_points))
fig.canvas.manager.set_window_title('Simple TinySA Spectrum display tool') 
ax_wfall.axis('off')

baseline_min_power = np.min(meas_power)
baseline_max_power = np.max(meas_power)

im = ax_wfall.imshow(wfall_buffer, aspect='auto', cmap='rainbow', vmin=baseline_min_power, vmax=baseline_max_power)
line, = ax_spec.plot([], [], lw=1, color='red')

ax_spec.grid(True)
ax_spec.set_xlabel("Frequency (MHz)")
ax_spec.set_ylabel("Power (dBm)")

set_lims = True

def animate_func(i):

    global wfall_buffer, set_lims, baseline_min_power, baseline_max_power
    wfall_buffer = np.roll(wfall_buffer, shift=1, axis=0)
    freq = np.linspace(f_low, f_high, N_points)
    meas_power = get_tinysa_scanraw(s_port, f_low, f_high, N_points, RBW)

    if np.min(meas_power)<(baseline_min_power-10) or np.max(meas_power)>baseline_max_power+10:
        set_lims = True
        baseline_min_power = np.min(meas_power)
        baseline_max_power = np.max(meas_power)

    wfall_buffer[0,:] = meas_power
    im.set_array(wfall_buffer)
    line.set_data(freq/1e6, meas_power)
    if set_lims:
        ax_spec.set_xlim(min(freq/1e6),max(freq/1e6))
        ax_spec.set_ylim(baseline_min_power-10, baseline_max_power+10)
        set_lims = False

    return [im]

anim = animation.FuncAnimation(fig, animate_func, frames = None)
                               
plt.show() 

