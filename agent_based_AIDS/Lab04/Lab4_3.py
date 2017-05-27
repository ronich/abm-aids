
# coding: utf-8

# # Zajęcia 4 cz.3

# ## 'Współprogramy'

# Typowym sposobem pisania programów komputerowych jest modularyzacja złożonego zadania obliczeniowego czyli jego podział na mniejsze, logicznie wyodrębnione jednostki. Jednostki takie przybierają w zależności od wybranego języka programowania formę funkcji, procedur albo klas.
# Po dekompozycji zadania obliczeniowego na moduły określa się sposób ich współpracy. Najczęściej koordynacje pracy modułów powierza się głównej funkcji sterującej (zwyczajowo nazywanej `main`). Funkcja sterująca okresla nastepstwo wykonania i zasady współpracy poszczególnych modułów przy użyciu (poznanych już) instrukcji warunkowych, petli itd. W takim podejściu moduły przyjęło się nazywać **podprogramami** (ang. *subroutine*).
# <img src='subroutine.png'style="max-width:30%;"/>

# Istnieje alternatywny sposób koordynacji pracy podzadań obliczeniowych bez użycia funkcji sterującej, w którym przebieg przetwarzania wynika wyłącznie z komunikacji między modułami. Przepływ sterowania w tym podejściu określa się przez łączenie zadań w łańcuchy (potoki). Takie podejście to nazywa się też czasami sterowaniem przez zdarzenia (ang. _event driven_). W takim podejściu moduły przyjęło się nazywać **współprogramami** (ang. *coroutine*). Jak się przekonamy podejście oparte o  współprogramy doskonale pasuje do modelowania złożonych systemów kolejkowych.
# <img src='coroutine.png'style="max-width:70%;"/>

# ### generatory - krótkie przypomnienie

# W pythonie *współprogramy* tworzymy w sposób zbliżony do generatorów. W istocie okazuje się, że generatory Pythona są szczególnym typem *współprogramów*.

# In[ ]:

g = (x**2 for x in range(10))
g


# In[ ]:

print(g)


# In[ ]:

g.__next__()


# In[ ]:

list(g)


# In[ ]:

g = (x**2 for x in range(10))
g


# In[ ]:

next(g)


# In[ ]:

def moj_generator():
    n = 0
    print('przed yield: n =', n)
    while True:
        n += 1
        yield n
        print('po yield: n =', n)


# In[ ]:

g = moj_generator()
g


# In[ ]:

next(g)


# przykład prostego 'koprogramu':

# In[ ]:

def my_coroutine():
    n = 0
    print('przed yield: n =', n)
    while True:
        n = yield n+1
        print('po yield: n =', n)


# In[ ]:

g = my_coroutine()
g


# przed pierwszym użyciem 'współprogram' trzeba zainicjować poleceniem `next` albo metodą `send(None)`

# In[ ]:

next(g)


# wartosci do *coroutine*m przekazujemy wywołując metodę `send(wartość)`

# In[ ]:

g.send(22)


# ###Produkuj-filtruj-konsumuj
# Typowym sposobem wykorzystania potoku przetwarzania jest wzorzec _'producent-konsument'_, w którym współprogram pełni jedną z trzech ról:
# - **producenta**, który generuje dane wejściowe dla potoku korzystając z medody `send()` 
# - **filtra**, który konsumuje i wstepnie przetwarza (np. filtruje, klasyfikuje itp.) dane wejsciowe, nastepnie przesyła je do przetwarzania na kolejnych etapach potoku korzystając z metod `yield()` i `send()`
# - **konsumenta**, który dokonuje końcowego przetwarzania danych otrzymanych z wykorzystaniem metody `yield()` i przekazuje je na wyjście potoku
# <img src='produce-filter-consume.png'style="max-width:90%;"/>
# Przyjrzyjmy się jak wzorzec 'producent-konsument' możemy wykorzytać do implementacji prostego systemu kolejkowego omawianego na poprzednich zajęciach.

# In[ ]:

import random as rnd
LAMBDA = 1

# konsument - odbiorca zgłoszeń
def server():
    end_time = 0
    start_time = 0
    while True:
        arrival_time = yield (start_time, end_time)
        start_time = max(arrival_time, end_time)
        service_time = rnd.expovariate(LAMBDA)
        end_time = start_time + service_time


# In[ ]:

# producent - generator zgłoszeń
def customers(N, server):
    arrival_time = 0
    print('arrival_time \t start_time \t end_time')
    for i in range(N):
        result = server.send(arrival_time)
        print('%05f \t %05f \t %05f' % (arrival_time, result[0], result[1]))
        arrival_time += rnd.expovariate(LAMBDA)


# In[ ]:

# tworzymy i inicjujemy serwer
s1 = server()
next(s1)


# In[ ]:

customers, server, s1


# In[ ]:

# symulacje jest uruchamiana i sterowana
# przez strumień zgłoszeń generowany przez producenta 
c = customers(10,s1)
c


# In[ ]:



