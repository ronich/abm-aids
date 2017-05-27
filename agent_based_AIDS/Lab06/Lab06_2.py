
# coding: utf-8

# # Zajęcia 6 cz.2

# ## pakiet [numpy](http://www.numpy.org/)
# Pakiet [numpy](http://www.numpy.org/) dostarcza prosty i intuicyjny interfejs obiektowy do pracy z danymi w postaci wektorów i macierzy. Podstawowym typem danych jest tablica (array) o okreslonych wymiarach. Przyklad ponizej ilustruje tworzenie wektora (tablicy 1. wymiarowej) na bazie istniejacej kolekcji danych:

# In[1]:

import numpy as np


# In[2]:

np.array(range(10))


# tę samą operaję możemy wykonać prościej jako:

# In[3]:

np.arange(10)


# funkcja 'arange' jest bardziej elastyczna od generatora 'range' gdyż pozwala na generowanie wartosci niecalkowitych:

# In[4]:

np.arange(0,1,.1)


# podobna role pelni funkcja 'linspace' ktora wypelnia wskazany zakres określoną iloscia (domyslnie 50) rownomiernie rozlozonych wezlow:

# In[5]:

np.linspace(0,1)


# wymiary talblicy przechowuje atrybut 'shape':

# In[6]:

u = np.arange(10)


# In[7]:

u.shape


# klasa 'array' przeciąża operatory arytmetyczne co pozwala na proste wykonywanie działań na elementach wektora:

# In[8]:

-u


# In[9]:

u+1


# In[10]:

v = np.arange(10)


# In[11]:

u+v


# In[12]:

u-v


# In[13]:

u*v


# jesli interesuje nas iloczyn wektorowy a nie Schura korzystamy z funkcji 'dot':

# In[14]:

u.dot(v)


# albo korzystamy z wyspecjalizowanej podklasy 'matrix' ktora przeciąża operatory w sposób właściwy dla algebry macierzy:

# In[15]:

u = np.matrix(u)
v = np.matrix(v)
u, v


# aby wykonac mnozenie wektorów wierszowych musimy dokonac transpozycji jednego z nich:

# In[16]:

u*v


# In[17]:

u*v.T


# w rownie prosty sposob wykonujemy inne funkcje na elementach tablic:

# In[18]:

np.sqrt(u)


# pakietu [numpy](http://www.numpy.org/) najwygodniej jest używać korzystając z IPythona w trybie emulacji matlaba. Użycie polecenia <tt>%pylab</tt> spowoduje zaimportowanie najbardziej przydatnych poleceń z pakietów <tt>numpy</tt> i <tt>matplotlib</tt> do globalnej przestrzeni nazw. W zamierzeniu środowisko ma przypominać to znane użytkownikom MatLaba:
# 
#     %pylab [--no-import-all] [gui]
#     Load numpy and matplotlib to work interactively.
#     This function lets you activate pylab (matplotlib, numpy and
#     interactive support) at any point during an IPython session.

# In[19]:

get_ipython().magic('pylab')


# ponieważ zawartość modułów jest importowana do globalnej przestrzeni nazw możemy pominąć przedrostki

# In[20]:

arange(10)


# #### Przyklady

# generowanie macierzy jednostkowej

# In[21]:

I = eye(5)
I


# generowanie macierzy losowej 3x3 ~U(0,1)

# In[22]:

random.rand(3,3)


# generowanie macierzy losowej 3x3 ~N(0,1)

# In[23]:

np.random.randn(3,3)


# generowanie macierzy losowej 5x5 z rozkł. dyskretnego ~U(0,10)

# In[24]:

C = random.randint(0,10,(5,5))
C


# trojkątna górna

# In[25]:

triu(C)


# trójkątna dolna

# In[26]:

tril(C)


# transpozycja

# In[27]:

transpose(C)


# In[28]:

C.T


# macierz odwrotna

# In[29]:

inv(C)


# In[30]:

C = matrix(C)
C.I


# dekompozycja według wartości osobliwych

# In[31]:

S,V,D = svd(C)
S,V,D


# In[32]:

X = svd(C)
X


# przekształcenie tablicy 1. wymiarowej w 2. wymiarową:

# In[33]:

A = arange(12)
B = arange(12)
A,B


# In[34]:

A = A.reshape(3,4)
B = B.reshape(4,3)
A


# In[35]:

B


# iloczyn Schura:

# In[36]:

A*B.T


# iloczyn macierzy:

# In[37]:

A = matrix(A)
B = matrix(B)


# In[38]:

A


# In[39]:

B


# In[40]:

C = A*B
C


# pakiet 'matplotlib' jest zintegrowany z pakietem 'numpy' co pozwala na proste generowanie wykresów:

# In[41]:

x = linspace(-pi,pi,50)
x


# In[42]:

plot(x,cos(x))
grid()


# polecenie 'meshgrid' generuje siatke interpolacyjna w dowolnej ilosci wymiarów:

# In[43]:

v = linspace(-pi,pi,200)
x,y = meshgrid(v, v)


# In[44]:

x


# In[45]:

y


# In[46]:

z = sin(x) + cos(y)

from mpl_toolkits.mplot3d import Axes3D
fig = figure()
ax = fig.gca(projection='3d')
ax.plot_surface(x, y, z, cmap='jet', linewidth=0.1, alpha = .75)


# pakiet numpy jest nie tylko prosty w użyciu ale też zoptymalizowany pod względem wydajności:

# In[47]:

def dot_prod(u,v):
    return sum([x*y for x,y in zip(u,v)])


# In[48]:

N = 10000
a = tuple(range(N))


# In[49]:

get_ipython().magic('timeit -n100 dot_prod(a,a)')


# In[50]:

a = arange(N)
get_ipython().magic('timeit -n100 a.dot(a)')


# jak widać w tym przypadku przyspieszenie w stosunku do 'naszej' implementacji iloczynu wektorowego wynosi ponad 170x!

# In[51]:

2430/8


# ## pakiet [scipy](http://www.scipy.org/)
# "_SciPy is a collection of mathematical algorithms and convenience functions built on the Numpy extension of Python. It adds significant power to the interactive Python session by providing the user with high-level commands and classes for manipulating and visualizing data. With SciPy an interactive Python session becomes a data-processing and system-prototyping environment rivaling sytems such as MATLAB, IDL, Octave, R-Lab, and SciLab._"

# In[52]:

def rosen(v):
    """The Rosenbrock function"""
    return (1-v[0])**2+100*(v[1]-v[0]**2)**2


# In[53]:

v = linspace(-1.5,1.5,200)
x,y = meshgrid(v, v)


# In[54]:

z = [rosen((x[i],y[i])) for i in range(len(x)) ]


# In[55]:

fig = figure()
ax = fig.gca(projection='3d')
ax.plot_surface(x, y, z, cmap='jet', linewidth=0.1, alpha = .75)


# In[56]:

from scipy.optimize import minimize
x0 = (-0.5, -2.7)
res = minimize(rosen, x0, method='nelder-mead', options={'xtol': 1e-8, 'disp': True})


# In[57]:

res

