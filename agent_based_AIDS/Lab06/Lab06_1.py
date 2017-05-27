
# coding: utf-8

# # Zajęcia 6 cz.1

# ##[matplotlib](http://matplotlib.org)
# [matplotlib](http://matplotlib.org) to biblioteka do generowania wykresów w Pythonie o [bogatych możliwościach](http://matplotlib.org/gallery.html). Nie jest ona częścią biblioteki standardowej ale jest domyślnie zainstalowana  w większości dystrybucji 'naukowych'.

# In[5]:

import math
import matplotlib.pyplot as plt


# In[6]:

x = [x/100 for x in range(1000)]
y = [math.sin(a) for a in x]


# In[7]:

plt.plot(x,y)


# In[9]:

import random
x = [random.randint(1,10) for x in range(100)]
y = [random.randint(1,10) for x in range(100)]


# In[10]:

plt.hist((x,y));


# Matplolitb dostarcza rozbudowane [API](http://matplotlib.org/api/index.html) (ang. _application programming interface_) ktore umozliwia bezposrednie manipulowanie poszczegolnymi elementami składowymi wykresu, reprezentowanymi przez obiekty klas pakietu <tt>matplotlib</tt>. Podstawowe klasy pakietu <tt>matplotlib</tt> ilustruje ponizszy diagram:
# <img src="fig_map.png">
# Ponizej kilka ciekawych przykładów ilustrujących możliwości API pakietu <tt>matplotlib</tt>:

# [integral_demo.py](integral_demo.py) - opisywanie wykresów z użyciem symboli matematycznych

# In[11]:

"""
Plot demonstrating the integral as the area under a curve.

Although this is a simple example, it demonstrates some important tweaks:

    * A simple line plot with custom color and line width.
    * A shaded region created using a Polygon patch.
    * A text label with mathtext rendering.
    * figtext calls to label the x- and y-axes.
    * Use of axis spines to hide the top and right spines.
    * Custom tick placement and labels.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def func(x):
    return (x - 3) * (x - 5) * (x - 7) + 85

a, b = 2, 9 # integral limits
x = np.linspace(0, 10)
y = func(x)

fig, ax = plt.subplots()
plt.plot(x, y, 'r', linewidth=2)
plt.ylim(ymin=0)

# Make the shaded region
ix = np.linspace(a, b)
iy = func(ix)
verts = [(a, 0)] + list(zip(ix, iy)) + [(b, 0)]
poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
ax.add_patch(poly)

plt.text(0.5 * (a + b), 30, r"$\int_a^b f(x)\mathrm{d}x$",
         horizontalalignment='center', fontsize=20)

plt.figtext(0.9, 0.05, '$x$')
plt.figtext(0.1, 0.9, '$y$')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')

ax.set_xticks((a, b))
ax.set_xticklabels(('$a$', '$b$'))
ax.set_yticks([])

plt.show()


# [scatter_demo.py](scatter_demo.py) - wykres punktowy

# In[12]:

"""
Demo of scatter plot

Size increases radially in this example and color increases with angle (just to
verify the symbols are being scattered correctly).
"""
import numpy as np
import matplotlib.pyplot as plt


N = 150
r = 2 * np.random.rand(N)
theta = 2 * np.pi * np.random.rand(N)
area = 300 * r**2 * np.random.rand(N)
colors = theta

ax = plt.subplot(111)
c = plt.scatter(theta, r, c=colors, s=area, cmap=plt.cm.hsv)
c.set_alpha(0.7)

plt.grid()
plt.show()


# [bar_demo.py](bar_demo.py) - wykres kolumnowy

# In[13]:

# %load bar_demo.py
"""
Demo of bar plot
"""
import numpy as np
import matplotlib.pyplot as plt


N = 20
theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
radii = 10 * np.random.rand(N)
width = np.pi / 4 * np.random.rand(N)

ax = plt.subplot(111)
bars = ax.bar(theta, radii, width=width, bottom=0.0)

# Use custom colors and opacity
for r, bar in zip(radii, bars):
    bar.set_facecolor(plt.cm.jet(r / 10.))
    bar.set_alpha(0.5)

plt.grid()
plt.show()


# [polar_demo.py](polar_demo.py) - powyższe wykresy we współrzędnych polarnych

# In[14]:

# %load polar_demo.py
"""
Demo of plot on a polar axis.
"""
import numpy as np
import matplotlib.pyplot as plt

# plot #1
N = 20
theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
radii = 10 * np.random.rand(N)
width = np.pi / 4 * np.random.rand(N)

ax = plt.subplot(121, polar=True)
bars = ax.bar(theta, radii, width=width, bottom=0.0)

# Use custom colors and opacity
for r, bar in zip(radii, bars):
    bar.set_facecolor(plt.cm.jet(r / 10.))
    bar.set_alpha(0.5)

# plot #2
N = 150
r = 2 * np.random.rand(N)
theta = 2 * np.pi * np.random.rand(N)
area = 200 * r**2 * np.random.rand(N)
colors = theta

ax = plt.subplot(122, polar=True)
c = plt.scatter(theta, r, c=colors, s=area, cmap=plt.cm.hsv)
c.set_alpha(0.75)
    
plt.show()


# [bayes_update.py](bayes_update.py) - wykres animowany, pokazuje ewolucje rozkładu _a posteriori_ wzgledem naplywajacych obserwacji (uruchomić na lokalnym komputerze)

# In[424]:

# %load bayes_update.py
# update a distribution based on new data.
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
from matplotlib.animation import FuncAnimation

class UpdateDist(object):
    def __init__(self, ax, prob=0.5):
        self.success = 0
        self.prob = prob
        self.line, = ax.plot([], [], 'k-')
        self.x = np.linspace(0, 1, 200)
        self.ax = ax

        # Set up plot parameters
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 15)
        self.ax.grid(True)

        # This vertical line represents the theoretical value, to
        # which the plotted distribution should converge.
        self.ax.axvline(prob, linestyle='--', color='black')

    def init(self):
        self.success = 0
        self.line.set_data([], [])
        return self.line,

    def __call__(self, i):
        # This way the plot can continuously run and we just keep
        # watching new realizations of the process
        if i == 0:
            return self.init()

        # Choose success based on exceed a threshold with a uniform pick
        if np.random.rand(1,) < self.prob:
            self.success += 1
        y = ss.beta.pdf(self.x, self.success + 1, (i - self.success) + 1)
        self.line.set_data(self.x, y)
        return self.line,

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ud = UpdateDist(ax, prob=0.7)
anim = FuncAnimation(fig, ud, frames=300, init_func=ud.init,
        interval=20, blit=True)
plt.show()


# [polar_anim_demo.py](./polar_anim_demo.py) - wykres animowany (uruchomić na lokalnym komputerze)

# In[418]:

"""
Demo of a line plot on a polar axis.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm

colors = cm.jet(np.linspace(0, 1, 60))

r = np.arange(0, 2.0, 0.01)
theta = 2 * np.pi * r

fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
line, = ax.plot(theta, r, linewidth=8, animated=True)
ax.set_rmax(2.0)
ax.grid(True)

def anim(i):
    global theta
    theta -= 1/(3*np.pi)
    line.set_xdata(theta)
    line.set_color(colors[i])
    return line,
    
ax.set_title("A line plot on a polar axis", va='bottom')
anim = FuncAnimation(fig, anim, frames=60, interval=15, blit=True,
                     repeat_delay=0)
plt.show()

