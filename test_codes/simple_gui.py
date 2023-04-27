from tkinter import * 
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import serial
from time import sleep
import numpy as np

freq = np.linspace(0,1,100)
power_meas = np.linspace(0,1,100)

fig = Figure(figsize = (5, 5), dpi = 100)
plot1 = fig.add_subplot(111)
plot1.plot(freq/1e6, power_meas)

fig2 = Figure(figsize = (5, 5), dpi = 100)
plot12 = fig2.add_subplot(111)
plot12.plot(freq/1e6, power_meas**2)

def plot():

    canvas = FigureCanvasTkAgg(fig,master = window)  
    canvas.draw()

    canvas.get_tk_widget().pack()

def change_plot():
    plt.close(fig)
    canvas = FigureCanvasTkAgg(fig2,master = window)  
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
plot_button.pack()

plot2_button = Button(master = window, 
                     command = change_plot,
                     height = 2, 
                     width = 10,
                     text = "Plot 2")
plot2_button.pack()
  
# run the gui
window.mainloop()