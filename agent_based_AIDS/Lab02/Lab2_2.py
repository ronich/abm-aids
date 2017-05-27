
# coding: utf-8

# # Zajęcia 2 c.d

# Przykład na potwierdzenie, że w Pythonie można napisać symulacje [DES](http://en.wikipedia.org/wiki/Discrete_event_simulation) prostego systemu kolejkowego [M/M/1](http://pl.wikipedia.org/wiki/M/M/1) w kilku liniach kodu

# In[1]:

# parametryzacja
N = 1000 # number of events (arrivals) to simulate
arrival_rate = 1 # parametr 'lambda' rozkladu wykladniczego, z ktorego generujemy kolejne zdarzenia
arrival = 0 # first arrival at time 0
endtime = 0 # init processing end time


# In[2]:

import random as rnd

# symulacja M/M/1
for i in range(N):
    arrival += rnd.expovariate(arrival_rate)
    starttime = max(arrival, endtime) # processing start time
    endtime = starttime + rnd.expovariate(1) # processing end time


# Zeby sie przekonac czy symulacja działa, zbierzmy kilka uzytecznych statystyk z jej przebiegu:

# In[24]:

arrival = 0 # first arrival at time 0
endtime = 0 # init processing end time
arrhist = [] # to store arrival history
endhist = [] # to store history of processing end times


# In[25]:

for i in range(N):
    arrival += rnd.expovariate(arrival_rate)
    starttime = max(arrival, endtime) # processing start time
    endtime = starttime + rnd.expovariate(1) # processing end time
    arrhist.append(arrival) # store arrival history
    endhist.append(endtime) # store end time history


# Wygenerujemy teraz wykres prezentujący dynamike dlugosci kolejki. Historie kolejnych zdarzen (pojawiania sie klientow w kolejce) mamy w wektorze `arrhist`. Dlugosc kolejki musimy niestety policzyc:

# In[26]:

qhist = [] # queue length history
for i in range(N):
    l = len([x for x in endhist[:i] if x >= arrhist[i]])
    qhist.append(l)


# Teraz mozemy juz wygenerowac wykres. Skorzystamy w tym celu z funkcji `plot` pakietu `matplotlib`.

# In[27]:

# queue length plot
from matplotlib.pyplot import plot
plot(arrhist, qhist) # queue length against arrival times


# Powyzsza implementacja systemu M/M/1 ma kilka wad. Główną jest to, że wymaga dodatkowego kodu do policzenia dlugosci kolejki. Sposób w jaki to robimy nie jest optymalny (prosze sprobowac zwiekszyc ilosc zdarzen dziesieciokrotnie i sprawdzic jak wplynie to na wydajnosc symulacji). Poprawimy kod. Skorzystamy z metod `append` i `pop`, ktore pozwalaja korzystac z list jak z kolejek:

# In[33]:

# parametryzacja
N = 1000 # number of events (arrivals) to simulate
arrival_rate = 1 # parametr 'lambda' rozkladu wykladniczego, z ktorego generujemy kolejne zdarzenia
arrival = 0 # first arrival at time 0
endtime = 0 # init processing end time

arrhist = [] # to store arrival history
qhist = []   # to store queue length history 
q = [] # The Queue


# In[36]:

for i in range(N):
    arrival += rnd.expovariate(arrival_rate)
    q.append(arrival)
    while endtime <= arrival:
        starttime = max(q.pop(0), endtime) # processing start time
        endtime = starttime + rnd.expovariate(1) # processing end time
    arrhist.append(arrival) # store arrival history
    qhist.append(len(q)) # store the queue size history


# jak widac moglismy bez istotnego wplywu na wydajnosc wykonac przebieg dla 100x wiekszej ilosci zdarzen! takze wygenerowanie wykresu nie sprawia juz trudnosci:

# In[37]:

plot(arrhist, qhist) # queue length against arrival times


# ## Rozkład wykładniczy
# Wyjaśnimy, dlaczego korzystamy z rozkładu wykładniczego do generowania czasu pomiedzy kolejnymi zdarzeniami w symulacji systemu kolejkowego. Skorzystamy z modułu `numpy`:

# In[38]:

from numpy.random import exponential
from numpy import cumsum


# Z rozkladu wykładniczego z parametrem $\lambda = 1$ wygenerujmy losowy wektor, który określi przerwy czasu pomiędzy kolejnymi klientami zjawiającymi się w kolejce

# In[39]:

arrivals = exponential(1,10000)


# dla jasnosci wyswietlamy histogram. Korzystamy z funkcji `hist` pakietu `matplotlib`:

# In[40]:

from matplotlib.pyplot import hist
hist(arrivals, 40);


# Jeśli teraz spojrzymy na rozkład tych zdarzeń na osi czasu symulacji, okaże sie ze jest on jednostajny:

# In[41]:

hist(cumsum(arrivals),40);


# wygenerowany w ten sposob przebieg zdarzeń jest realizacją [procesu Poissona](http://pl.wikipedia.org/wiki/Proces_Poissona).

# ## odpowiedź
# na pytanie z poprzednich zajec:

# In[18]:

v = 'Ala ma kota'.split()
v


# In[19]:

u = [v,v]
u


# In[20]:

[[x.replace('a','*') for x in y] for y in u]


# ## zasięg zmienych i przestrzenie nazw
# Do tej pory pracujac w trybie interaktywnym Pythona definiowalismy zmienne w domyslnej **globalnej** przestrzeni nazw dzieki czemu byly one 'widoczne' i dostepne w kazdym fragmencie kodu

# In[21]:

a = -1
a


# In[22]:

for a in range(5):
    print(a,end=' ')
a


# Jak widac w powyzszym przykladzie zmienna <tt>'a'</tt>, ktora zainicjowalismy wartoscia -1 i zmienna <tt>'a'</tt> ktorej uzylismy jako licznika petli to ta sama zmienna. 
# 
# Natomiast w ponizszym przykladzie widzimy, ze zmienna <tt>'a'</tt> zainicjowana wewnatrz funkcji i zmienna <tt>a = -1</tt> zainicjowana wyzej to dwie rozne zmienne - pomimo zbieznosci nazw. Jest tak dlatego, ze zmienna <tt>'a'</tt> zainicjowana wewnatrz funcji jest tworzona w _lokalnej_ dla funkcji <tt>f()</tt> przestrzeni nazw. Zmienne o tej samej nazwie ale tworzone w odrebnych przestrzeniach sa roznymi zmiennymi.
# Definiujac zmienne w ciele funkcji musimy pamietac, ze ich zasieg jest lokalny a czas zycia ograniczony - sa one tworzone w momencie wywolania funkcji i 'niszczone' kiedy funkcja konczy dzialanie.

# In[23]:

a = -1
def f():
    a = 2
    return a

f(), a


# Przekazanie zmiennej globalnej na liscie parametrow funkcji nie zmienia tej zasady. Ponizej widzimy ze zmienna <tt>'a'</tt> bedaca parametrem funkcji ma zasieg lokalny i zmiana jej wartosci wewnatrz funkcji nie ma wplywu na wartosc zmiennej gloablnej. Ponownie zbieznosc nazw nie oznacza tozsamosci zmiennych.

# In[24]:

def f(a):
    a = a + 1
    return a
f(a), a


# In[25]:

def f(a):
    a += 1
    return a
f(a), a


# sprobujmy 'dobrac sie' do zmiennej globalnej <tt>'a'</tt> jak w ponizszym przykladzie:

# In[26]:

def f():
    a += 1
    return a
f(), a


# Python zglosil blad poniewaz nie odnalazl zmiennej <tt>'a'</tt>, ktorej wartosc chcemy zwiekszyć, w _lokalnej_ przestrzeni nazw funkcji <tt>f()</tt>. Musimy zatem jawnie wskazac, ze chodzi nam o zmienna <tt>'a'</tt>, ktora istnieje w _globalnej_ przestrzeni nazw. Robimy to korzystajac z modyfikatora <tt>'global'</tt>:

# In[27]:

def f():
    global a
    a += 1
    return a
f(), a


# Jak widac tym razem zmianie ulegla wartosc _globalnej_ zmiennej <tt>'a'</tt>. 
# 
# Klauzuli <tt>'global'</tt> nie musimy uzywac jesli chcemy tylko _odczytac_ wartosc zmiennej globalnej. W takim przypadku Python odszuka zmienną o podanej nazwie w przestrzeni globalnej jesli nie znajdzie jej w lokalnej przestrzeni nazw funkcji:

# In[28]:

def f():
    b = a + 1
    return b
f(), a


# lub prosciej:

# In[29]:

def f():
    return a + 1
f(), a


# W skrocie mozna to ujac tak - operator przypisania tworzy zmienna w lokalnej dla bloku kodu w ktorym sie znajdujemy przestrzeni nazw. Jesli z jakiegos powodu chcemy "dobrać się" do zmiennej z innej przestrzeni nazw korzystamy z modyfikatora zakresu <tt>'global'</tt> albo <tt>'[nonlocal](http://docs.python.org/3/tutorial/classes.html#scopes-and-namespaces-example)'</tt>. Możemy też jawnie podac identyfikator przestrzeni nazw ktora nas interesuje co wyjasnimy wkrótce.

# ##'pass by value' i 'pass by reference'
# Powyżej omówione zasady opisują zachowanie zmiennych skalarnych. Zachowanie zmiennych będących kolekcjami jest nieco inne. Porownajmy ponizszy przyklad z wczesniejszymi przykladami:

# In[31]:

def f(lista):
    lista = list(range(10,15))
    return lista


# In[32]:

lista = list(range(5))
f(lista), lista


# Jak na razie bez niespodzaianek - lista utworzona w obrebie funkcji ma lokalny zasieg i nie nadpisuje wartosci listy globalnej. Ale spojrzmy na ponizszy przyklad:

# In[33]:

def f(lista):
    lista[0] = 1
    return lista


# In[34]:

a = list(range(5))
a


# In[35]:

f(a), a


# Tym razem zmianie ulegla zawartosc _globalnej_ listy `a` mimo ze poslużylismy sie lokalną zmienną `lista` w przestrzeni nazw funkcji. Dlaczego tak sie stalo? Najprosciej mozna to wyjasnic mowiac, ze zmienne typu skalarnego (int, float, complex) sa przekazywane przez **wartość** (ang. *by value*) a zmienne typow zlozonych przez **odwołanie** (ang. _by reference_). Mowiac inaczej zmienne typu zlozonego przekazują _adres_ obszaru pamieci komputera, pod którym składowane są dane zawarte w kolekcji. Stosowanie notacji tablicowej takie jak `lista[1]`, które oznacza 'drugi element pod adresem wskazanym przez zmienną `lista`, pozwala zatem na bezposredni dostęp do tych danych. 
# 
# Aby zabezpieczyc dane w kolekcjach przed niezamierzonym nadpisaniem mozemy w wywolaniach przekazywac ich _kopie_. Najprostszym sposobem wykonania kopii kolekcji jest zastosowanie operatora `':'`. W przykladzie ponizej zmienne `a` i `b` wskazuja na ten sam adres w pamieci. Modyfikacja listy z uzyciem dowolnej z nich bedzie zatem odzwierciedlona przez obie zmienne:

# In[36]:

a = list(range(5))
a


# In[37]:

b = a
a, b


# In[38]:

a[1] = 'a'
a, b


# In[39]:

b[2] = 'b'
a, b


# aby temu zapobiec niech `'b'` bedzie kopia `'a'`:

# In[40]:

a = list(range(5))
a


# In[41]:

b = a[:]
a, b


# In[42]:

a[1] = 'a'
a, b


# In[43]:

b[2] = 'b'
a, b


# jesli elementami kolekcji sa inne kolekcje sprawa jest nieco bardziej zlozona.

# In[44]:

a = [1,2,3,['A','B']]
a


# In[45]:

# b jest kopią a
b = a[:]
a, b


# In[46]:

a[1] = 100
b[1] = 200
a, b


# jak na razie bez niespodzianek. ale spojrzmy:

# In[47]:

a[3][0] = 'C'
a, b


# jak widac operator <tt>':'</tt> skopiowal tylko skalarne elementy listy <tt>':'</tt>, ale nie skopiował elementów listy zagnieżdżonej! jest to tzw. 'płytka' kopia kolekcji. aby skopiowac pełne 'drzewo' kolekcji musimy wykonać kopię 'głęboką':

# In[48]:

import copy
b = copy.deepcopy(a)
a, b


# In[49]:

b[3][1] = 'D'
a, b


# ##Obsługa wyjątków
# Wyjątek to błąd który powstaje _w trakcie działania programu_ (dla odrożnieniena od błędów ktory popełniamy w trakcie pisania kodu).

# In[52]:

liczba = int(input("Podaj liczbę: "))
print("10 podzielone przez", liczba, "równa się", 10/liczba)


# Do przechwytywania wyjatkow sluzy instrukcja **`try/except`**:
# 
# ```python
#     try:
#         <operacje-mogące-rzucić-wyjątek>
#     except <typ-wyjątku-1> [ as <nazwa-zmiennej> ]:
#         # Tutaj przechwytujemy wyjątek typu typ-wyjątku-1
#         <operacje-zaradcze>
#     except <typ-wyjątku-2>, <typ-wyjątku-3> [ as <nazwa-zmiennej> ]:
#         # Tutaj przechwytujemy wyjątek typu typ-wyjątku-2
#         # lub typ-wyjątku-3.
#         <operacje-zaradcze>
#     except Exception [ as <nazwa-zmiennej> ]:
#         # Tutaj przechwytujemy wyjątek każdego innego typu 
#         <operacje-zaradcze>
#     finally:
#         # Tutaj należy wpisać działania takie jak zamknięcie plików
#         # i zwolnienie blokad, które muszą być wykonane zawsze 
#         # niezależnie od tego czy operacja się powiodła czy też nie.
#         <operacje-wykonywane-zawsze>
# ```
# 

# In[53]:

try:
    liczba = int(input("Podaj liczbę: "))
    print("10 podzielone przez", liczba, "równa się", 10/liczba)
except (ZeroDivisionError) as e:
    print(e, ': nie dzielimy przez zero!')


# Istotna jest kolejnosc klauzul except. Na poczatku wyłapujemy wyjątki najbardziej szczegołowe, w dalszej kolejnosci bardziej ogólne. W ustaleniu własciwej kolejności pomocna jest [hierarchia wyjątków](http://docs.python.org/3/library/exceptions.html#exception-hierarchy)

# In[55]:

# nieprawidlowa kolejnosc klauzul except
try:
    liczba = int(input("Podaj liczbę: "))
    print("10 podzielone przez", liczba, "równa się", 10/liczba)
except Exception:
    print('jakis wyjatek ale nie wiem jaki')
except (ZeroDivisionError) as e:
    print(e, ': nie dzielimy przez zero!')
except (ValueError) as e:
    print(e, ': zly format liczby')


# In[56]:

# prawidlowa kolejnosc klauzul except
try:
    liczba = int(input("Podaj liczbę: "))
    print("10 podzielone przez", liczba, "równa się", 10/liczba)
except (ZeroDivisionError) as e:
    print(e, ': nie dzielimy przez zero!')
except (ValueError) as e:
    print(e, ': zly format liczby')
except Exception:
    print('inny wyjatek')


# dopuszczalna jest tez ponizsza forma instrukcji try/except przechwytująca **wszystkie** wyjątki ale **należy jej  <font color="red">unikać</font>** ponieważ uniemożliwia zatrzymanie pracy programu sposobem innym niz ubicie procesu (jesli użyta w pętli):

# In[ ]:

while True:
    try:
        liczba = int(input("Podaj liczbę: "))
        print("10 podzielone przez", liczba, "równa się", 10/liczba)
    except:
        print('jakis wyjatek ale nie wiem jaki')


# można też ponownie 'rzucić' przechwycony wyjątek. służy do tego komenda <tt>'raise'</tt>

# In[1]:

# prawidlowa kolejnosc klauzul except
try:
    liczba = int(input("Podaj liczbę: "))
    print("10 podzielone przez", liczba, "równa się", 10/liczba)
except ZeroDivisionError as e:
    print(e, ': nie dzielimy przez zero!')
    raise
except ValueError as e:
    print(e, ': zly format liczby')
    raise
except Exception:
    print('inny wyjatek')
    raise


# polecenie <tt>'raise'</tt> służy również do 'rzucania' wyjatków na żądanie:

# In[1]:

wiek = 0
while not wiek:
    try:
        wiek = int(input("Podaj wiek: "))
        if wiek < 0:
            wiek = 0
            raise ValueError('Wiek nie może być ujemny')        
    except Exception as e:
        print(e)


# ### [Hierarchia wyjątków](http://docs.python.org/3/library/exceptions.html#exception-hierarchy)
#     BaseException
#      +-- SystemExit
#      +-- KeyboardInterrupt
#      +-- GeneratorExit
#      +-- Exception
#           +-- StopIteration
#           +-- ArithmeticError
#           |    +-- FloatingPointError
#           |    +-- OverflowError
#           |    +-- ZeroDivisionError
#           +-- AssertionError
#           +-- AttributeError
#           +-- BufferError
#           +-- EOFError
#           +-- ImportError
#           +-- LookupError
#           |    +-- IndexError
#           |    +-- KeyError
#           +-- MemoryError
#           +-- NameError
#           |    +-- UnboundLocalError
#           +-- OSError
#           |    +-- BlockingIOError
#           |    +-- ChildProcessError
#           |    +-- ConnectionError
#           |    |    +-- BrokenPipeError
#           |    |    +-- ConnectionAbortedError
#           |    |    +-- ConnectionRefusedError
#           |    |    +-- ConnectionResetError
#           |    +-- FileExistsError
#           |    +-- FileNotFoundError
#           |    +-- InterruptedError
#           |    +-- IsADirectoryError
#           |    +-- NotADirectoryError
#           |    +-- PermissionError
#           |    +-- ProcessLookupError
#           |    +-- TimeoutError
#           +-- ReferenceError
#           +-- RuntimeError
#           |    +-- NotImplementedError
#           +-- SyntaxError
#           |    +-- IndentationError
#           |         +-- TabError
#           +-- SystemError
#           +-- TypeError
#           +-- ValueError
#           |    +-- UnicodeError
#           |         +-- UnicodeDecodeError
#           |         +-- UnicodeEncodeError
#           |         +-- UnicodeTranslateError
#           +-- Warning
#                +-- DeprecationWarning
#                +-- PendingDeprecationWarning
#                +-- RuntimeWarning
#                +-- SyntaxWarning
#                +-- UserWarning
#                +-- FutureWarning
#                +-- ImportWarning
#                +-- UnicodeWarning
#                +-- BytesWarning
#                +-- ResourceWarning
