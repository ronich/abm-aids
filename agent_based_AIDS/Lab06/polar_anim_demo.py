"""
Demo of a line plot on a polar axis.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm

colors = cm.jet(np.linspace(0, 1, 60))
#colors = np.concatenate((colors, cm.jet(np.linspace(1, 0, 40))))

r = np.arange(0, 2.0, 0.01)
theta = 2 * np.pi * r

fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
line, = ax.plot(theta, r, linewidth=8, animated=True)
#ax.plot(theta-1, r, color='g', linewidth=3, animated=True)
ax.set_rmax(2.0)
ax.grid(True)

#colors = ('r','b','g')

def anim(i):
    global theta
    theta -= 1/(3*np.pi)
    line.set_xdata(theta)
#    xdata = line.get_xdata(orig=True)
#    xdata -= 1/(3*np.pi)
#    line.set_xdata(xdata)
#    line.set_xdata(theta-i/(3*np.pi))
    line.set_color(colors[i])
    return line,
    
ax.set_title("A line plot on a polar axis", va='bottom')
anim = FuncAnimation(fig, anim, frames=60, interval=15, blit=True,
                     repeat_delay=0)
plt.show()
