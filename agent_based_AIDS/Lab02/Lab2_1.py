
# coding: utf-8

# # Zajęcia 2

# ##Formatowanie ciągów znakowych - instrukcja `print()`
# Do tej pory korzystaliśmy z prostej składni intrukcji `print()`, w której kolejne parametry oddzielaliśmy przecinkiem:

# In[ ]:

a = 1234
b = 1/3
print('Zmienna a =', a, 'jest typu', type(a), ', zmienna B ma typ', type(b),
      'i zawartosc', b)


# ###'Stary' styl formatowania
# Python oferuje jeszcze dwa alternatywne sposoby formatowania ciagów znakowych - pierwszy ('stary') sposób ma składnie podobną do instrukcji `printf()` języka C. O szczegółach można przeczytać [w dokumentacji](http://docs.python.org/3/library/stdtypes.html#old-string-formatting). Przykład:

# In[ ]:

c = 1/2
c


# In[ ]:

print('c = %.6f' % c)


# In[ ]:

d = {'language': "Python", "number": 2}


# In[ ]:

print('%(language)s has %(number)03d quote types.' 
      % d)


# ###'Nowy' styl formatowania
# Drugi ('nowy') styl formatowania jest specyficzny dla Pythona. O szczegółach można przeczytać [w dokumentacji](http://docs.python.org/3/library/string.html#formatstrings). Przykład:

# In[ ]:

print('c = ', c, 'a = ', a)


# In[ ]:

print('c = {0}, a = {1}'.format(a,c))


# In[ ]:

c = 1/3
print('c = {0:.4}, a = {1:*^10}'.format(c, a))


# In[ ]:

print('c = {}, a = {}'.format(c, a))


# In[ ]:

print('c = {0:.4}, a = {1:*^10}'.format(c, a))


# In[ ]:

d = {'language': "Python", "number": 2}
d.values()


# In[ ]:

print('{} has {} quote types.'.format(*d.values()))


# # Funkcje
# Definicje funkcji w Pythonie rozpoczynamy slowem kluczowym `def`

# In[ ]:

def suma(a,b):
    return a+b


# In[ ]:

suma(3,5)


# In[ ]:

suma(3,5,4)


# argumentom mozemy nadawac wartosci domyslne

# In[ ]:

def suma(a,b,c=0):
    return (a+b+c)


# In[ ]:

suma(1,2)


# In[ ]:

suma(1,2,3)


# In[ ]:

suma('Ala','ma','kota')


# argumenty opcjonalne umieszczamy po argumentach wymaganych

# In[ ]:

def suma(a,b=0,c): # błąd!
    return (a+b+c)    


# argumentow nie musimy podawac 'jawnie' - mozemy uzyc w tym celu sekwencji

# In[ ]:

args = (2,3,4)
args, type(args)


# In[ ]:

suma(*args)


# argumenty mozna tez przekazywac po nazwie

# In[ ]:

suma(c=1,b=3,a=2)


# argumenty nazwane mozna przekazywac w formie slownika

# In[ ]:

args = zip(('c','a','b'), (1,3,2))
kwargs = dict(args)
kwargs


# In[ ]:

args = zip(('c','a','b','f'), (1,3,2,8))
kwargs = dict(args)
kwargs


# In[ ]:

suma(**kwargs)


# co bedzie jesli nie zgadza sie ilosc argumentow?

# In[ ]:

args = (2,3,4,5)
type(args)
suma(*args)


# mozemy tez zadeklarowac zmienna liczbe argumentow

# In[ ]:

def suma(*args):
    wynik = 0
    for x in args:
        wynik += x
    return wynik


# In[ ]:

suma(3,2)


# In[ ]:

suma(3,2,3,4,5,66,5)


# In[ ]:

def suma(a, *args):
    wynik = a
    for x in args:
        wynik += x
    return wynik


# In[ ]:

suma()


# In[ ]:

argumenty = tuple(range(10))
argumenty


# In[ ]:

suma(*argumenty)


# In[ ]:

suma(*range(10))


# In[ ]:

suma(*range(100))


# ## Funkcje [anonimowe (lambda)](http://pl.wikibooks.org/wiki/Zanurkuj_w_Pythonie/Wyra%C5%BCenia_lambda)
# Funkcje anonimowe sa uproszczonym schematem definiowania funkcji. Stosujemy je kiedy dla wygody pewnym wyrazeniom chcemy nadac postac funkcji. Tworzymy je slowem kluczowym <tt>'lambda'</tt>. Ogólna struktura jest nastepujaca:
#     
# ```python
# <nazwa_funkcji> = lambda <zmienne_wejsciowe>: <wyrazenie>
# ```

# In[ ]:

# pełna deklaracji funkcji f()
def f(x):
    return x**2

f(10)


# In[ ]:

# wersja lambda
g = lambda x: x**2

g(10)


# In[ ]:

type(f), type(g)


# In[ ]:

# wersja lambda
g = lambda x,y: x+y

g(10,20)


# In[ ]:

# wersja lambda
g = lambda *args: sum(args)

g(*range(100))


# z punktu widzenia Pythona funkcje nazwane i anonimowe sa równoważne:

# In[ ]:

type(f), type(g)


# In[ ]:

f,g


# ciekawe efekty mozna osiagnac łącząc funkcje lambda i [wyrażenia warunkowe](#wyr_war):

# In[ ]:

s = lambda x: "" if x == 1 else ("i" if x in {2,3,4} else "ów")


# In[ ]:

type(s)


# In[ ]:

for count in range(15):
    print("przetworzono {0} plik{1}".format(count, s(count)))


# ##generatory
# Generatory sa specjalnym rodzajem funkcji, ktore generują ciąg wartosci zgodnie z ustalonym algorytmem. Kolejne wartości ciagu sa generowane _na żądanie_ dzieki czemu oszczedzamy pamiec operacyjna (nie musimy przechowywac wartosci ciagu w pamieci).
# Poznalismy juz jeden z wbudowanych typow generatora - funkcję `range()`.
# Generatory definiujemy podobnie jak funkcje zastepujac slowo kluczowe `return` slowem `yield`.

# In[ ]:

# trywialny generator
def mojGenerator(n):
    for i in range(n):
        yield i**2


# In[ ]:

g = mojGenerator(12)


# In[ ]:

print(*g)


#  W odroznieniu od funkcji generatory przechowuja _stan_ pomiedzy wywolaniami - kolejne wywolanie zwracaja kolejne wartosci z ciagu:

# In[ ]:

g = mojGenerator(20)


# In[ ]:

for i in g:
    print(i, end = ' ')
    if i > 80: 
        break


# In[ ]:

print(*g)


# a po wyczerpaniu ciagu generator nie zwroci nic :)

# In[ ]:

list(g)


# generatory mozna tez definiowac w uproszczony sposob podobnie jak listy składane

# In[ ]:

generator = (x**2 for x in range(20))
print(generator)


# In[ ]:

for i in generator:
    print(i, end = ' ')
    if i > 80: 
        break


# In[ ]:

list(generator)


# In[ ]:

list(generator)


# ##dokumentowanie kodu
# Dokumentowanie kodu jest dobra praktyką, która pomaga innym użytkownikom kodu (oraz nam samym po upływie pewnego czasu) w jego zrozumieniu. W Pythonie funkcje dokumentujemy umieszczając opis funkcji i jej paramtetrów jako ciąg tekstowy w linii nastepującej po poleceniu <tt>'def'</tt>. Zgodnie z konwencja pierwsza linia to krotki opis funkcji, potem jedna linia pusta i bardziej rozbudowany opis funkcji i jej parametrow ponizej.

# In[ ]:

def f():
    '''Ta funkcja nie robi nic!
       
       Ta funkcja ma wyłącznie cel pedagogiczny:
       1. nie pobiera żadnych parametrów
       2. nie robi nic pożytecznego
       3. ale za to jest dobrze udokumentowana :P'''
    pass


# In[ ]:

help(f)


# In[ ]:

f


# dokumentacja jest dowolnym opisem ale najlepiej jest stosować format zgodny ze 'standardem' Pythona. Można się z nim zapoznać przegladając dokumentację przykladowych funkcji

# In[ ]:

help(print)


# In[ ]:

help(max)


# In[ ]:

help(suma)


# In[ ]:

def suma(first, second, third):
    '''return sum of three numeric values
       
       first:  1st element
       second: 2nd element
       third:  3rd element
       '''
    return (a+b+c)  


# In[ ]:

help(suma)


# In[ ]:

suma


# ## polecenie `import`
# Po uruchomienie interpretera Pythona mamy do dyspozycji pewien zbiór domyślnych poleceń i funkcji. Kiedy chcemy używać Pythona w wyspecjalizowanej dziedzinie, na przykład do bardziej złożonych obliczeń, pojawia się pytanie skąd wziąć potrzebne algorytmy?

# In[ ]:

sin(0)


# Twórcy Pythona chwalą się, że dostarczają go z ['bateriami w zestawie'](http://docs.python.org/3.4/tutorial/stdlib.html#batteries-included). Oznacza to, że mamy do dyspozycji bogatą [bibliotekę](http://docs.python.org/3.4/library/index.html) gotowych algorytmów do różnych zastosowań. Biblioteka ta jest podzielona na dziedzinowe pakiety, które z kolei dzielą sie na moduły. Dostęp do funkcji zawartych w poszczególnych modułach uzyskujemy poleceniem `import`. Omówimy krótko wybrane moduły.

# ##math
# moduł zawiera podstawowe funkcje matematyczne oraz definiuje stałe $\pi$ i $e$

# In[ ]:

import math

# In[ ]:
#zaimportowanie funkcji sin z math bezpośrednio do globalnej przestrzeni nazw

from math import sin

# In[ ]:
#zaimportowanie wszystkich funkcji bezposrednio do globalnej przestrzeni nazw

from math import *

# In[ ]:

help(math)


# po zaimportowaniu modułu dostep do jego zawartosci uzyskujemy podając nazwę funkcji poprzedzona nazwa modułu, którą w Pythonie nazywamy *przestrzenią nazw*:

# In[ ]:

math.pi, math.e


# In[ ]:

math.log(math.e)


# In[ ]:

math.cos(0)


# In[ ]:

math.sin(1/2*math.pi)


# ##random
# 
# Moduł do generowania liczb pseudolosowych

# In[ ]:

import random


# In[ ]:

help(random)


# liczba losowa z przedziału $[0, 1)$:

# In[ ]:

random.random()


# ustawianie ziarna losowego:

# In[ ]:

random.seed(1)


# liczba losowa całkowita z przedziału $[a, b]$:

# In[ ]:

random.randint(0,100)


# liczba losowa z rozkładu normalnego o parametrach $(\mu, \sigma)$:

# In[ ]:

random.gauss(0,1)


# losowa permutacja sekwencji (zmienia porządek sekwencji):

# In[ ]:

a = list(range(20))
print(a)


# In[ ]:

random.shuffle(a)
print(a)


# dla wygody możemy zmienic nazwę *przestrzeni nazw* do której wczytujemy zawartość modułu:

# In[ ]:

import random as rnd


# In[ ]:

a = [rnd.randrange(0,100) for x in range(10)]
a


# In[ ]:

rnd.randrange


# In[ ]:

rnd.shuffle(a)
a


# możemy też zaimportować wybrane elementy modułu do bieżącej przestrzeni nazw:

# In[ ]:

from random import randint


# In[ ]:

randint(1,100)


# Możliwe jest też zaimportowanie wszytkich składowych modułu do bieżącej przestrzeni nazw. Należy jednak pamietać, że może to doprowadzić do kolizji identyfikatorów (jeśli w bieżącej przestrzeni nazw istnieją identyfikatory takie jak w module to zostaną one 'przesłonięte')

# In[ ]:

from random import *


# In[ ]:

shuffle(a)
a


# ##time
# moduł zawiera funkcje do manipulacji datami i czasem

# In[ ]:

import time


# In[ ]:

help(time)


# czas bieżący w formacie 'timestamp' (ilość sekund od 'dnia zero'):

# In[ ]:

time.time()


# konwersja wartosci 'timestamp' do formatu 'human readable':

# In[ ]:

time.ctime(time.time())


# kiedy był ['dzień zero'](http://en.wikipedia.org/wiki/Epoch_%28reference_date%29#Computing)?

# In[ ]:

time.ctime(0)


# licznik czasu o wysokiej precyzji -- przydatny do mierzenia interwałów czasowych w przebiegu symulacji:

# In[ ]:

time.perf_counter()


# In[ ]:

time.perf_counter() - time.perf_counter()


# In[ ]:

print('%.12f' % (time.perf_counter() - time.perf_counter()))


# In[ ]:

print('%.12f' % (time.time() - time.time()))


# In[ ]:

print('%.12f' % (time.process_time() - time.process_time()))


# In[ ]:

time.process_time() - time.process_time()


# czas bieżący (lokalny) w postaci krotki nazwanej ([named tuple](http://docs.python.org/3.4/library/collections.html#namedtuple-factory-function-for-tuples-with-named-fields)):

# In[ ]:

a = time.localtime()
a


# In[ ]:

a.tm_year, a[1]


# In[ ]:

a[:]

