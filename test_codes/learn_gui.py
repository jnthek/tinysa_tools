from tkinter import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import serial
from time import sleep
import numpy as np

def get_tinysa_data(my_command):
    ser = serial.Serial(port='/dev/cu.usbmodem4001', baudrate=115200)
    ser.timeout = 0.05
    ser.write(str(my_command + "\r").encode('ascii'))
    result = ""
    data = ""
    sleep(0.05)
    while data != "ch> ":
        data = ser.readline().decode('ascii')
        result += data
    values = result.split("\r\n")
    ser.close() 
    return values

def plot():
  
    freq = np.array(get_tinysa_data("frequencies")[1:-1], dtype=np.float64)
    power_meas = np.array(get_tinysa_data("data 2")[1:-2], dtype=np.float64)
    
    fig = Figure(figsize = (5, 5), dpi = 100)
    plot1 = fig.add_subplot(111)
    plot1.plot(freq/1e6, power_meas)
    canvas = FigureCanvasTkAgg(fig,master = window)  
    canvas.draw()

    canvas.get_tk_widget().pack()

window = Tk()
  
# setting the title 
window.title('Plotting in Tkinter')
  
# dimensions of the main window
window.geometry("500x500")
  
# button that displays the plot
plot_button = Button(master = window, 
                     command = plot,
                     height = 2, 
                     width = 10,
                     text = "Plot")
  
# place the button 
# in main window
plot_button.pack()
  
# run the gui
window.mainloop()