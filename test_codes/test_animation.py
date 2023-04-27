import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N_points = 251
N_tstamps = 251

wfall_buffer = np.zeros([N_tstamps,N_points])
freq = np.linspace(87,108,N_points)

fig, [ax_spec, ax_wfall] = plt.subplots(2, 1, figsize=(16,9))
fig.canvas.manager.set_window_title('TinySA Spectrum Display tool') 
ax_wfall.axis('off')

im = ax_wfall.imshow(wfall_buffer, aspect='auto', cmap='rainbow', vmin=-1, vmax=10)
line, = ax_spec.plot([], [], lw=1, color='red')
ax_spec.grid(True)
ax_spec.set_xlabel("Freq (MHz")
ax_spec.set_ylabel("Power (dBm)")
spec_line = np.zeros(N_points)
spec_line[int(N_points/2)] = 20.0

def animate_func(i):

    global wfall_buffer
    global freq
    wfall_buffer = np.roll(wfall_buffer, shift=1, axis=0)

    my_data = np.random.normal(0,1,N_points) + spec_line
    wfall_buffer[0,:] = my_data
    im.set_array(wfall_buffer)
    line.set_data(freq, my_data)
    ax_spec.set_xlim(min(freq),max(freq))
    ax_spec.set_ylim(-5,5)

    return [im]

anim = animation.FuncAnimation(fig, animate_func, frames = None)
                               
plt.show() 