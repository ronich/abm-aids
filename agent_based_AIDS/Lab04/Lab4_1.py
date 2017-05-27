
# coding: utf-8

# # Zajęcia 4

# ##Formatowanie ciągów znakowych - instrukcja `print()`
# Do tej pory korzystaliśmy z prostej składni intrukcji `print()`, w której kolejne parametry oddzielaliśmy przecinkiem:

# In[ ]:

kot = 'kota'


# In[ ]:

print('Ala', 'ma', kot)


# In[ ]:

a = 1234
b = 1/3
print('Zmienna a =', a, 'jest typu', type(a), ', zmienna B ma typ', type(b),
      'i zawartosc', b)


# ###'Stary' styl formatowania
# Python oferuje jeszcze dwa alternatywne sposoby formatowania ciagów znakowych - pierwszy ('stary') sposób ma składnie podobną do instrukcji `printf()` języka C. O szczegółach można przeczytać [w dokumentacji](http://docs.python.org/3/library/stdtypes.html#old-string-formatting). Przykład:

# In[ ]:

c = 1/3
c


# In[ ]:

print('c = %.4f' % c)


# In[ ]:

d = {'language': "Python", "number": 2}


# In[ ]:

print('%(language)s has %(number)03d quote types.' % d)


# ###'Nowy' styl formatowania
# Drugi ('nowy') styl formatowania jest specyficzny dla Pythona. O szczegółach można przeczytać [w dokumentacji](http://docs.python.org/3/library/string.html#formatstrings). Przykład:

# In[ ]:

print('c = ', c, 'a = ', a)


# In[ ]:

print('c = {0}, a = {1}'.format(a,c))


# In[ ]:

c = 1/3
print('c = {0:.4}, a = {1:+^10}'.format(c, a))


# In[ ]:

print('c = {}, a = {}'.format(c, a))


# In[ ]:

print('c = {0:.4}, a = {1:*^10}'.format(c, a))


# In[ ]:

d = {'language': "Python", "number": 2}
d.values()


# In[ ]:

print('{} has {} quote types.'.format(*d.values()))


# In[ ]:

help(str)


# ##dokumentowanie kodu
# Dokumentowanie kodu jest dobra praktyką, która pomaga innym użytkownikom kodu (oraz nam samym po upływie pewnego czasu) w jego zrozumieniu. W Pythonie funkcje dokumentujemy umieszczając opis funkcji i jej paramtetrów jako ciąg tekstowy w linii nastepującej po poleceniu <tt>'def'</tt>. Zgodnie z konwencja pierwsza linia to krotki opis funkcji, potem jedna linia pusta i bardziej rozbudowany opis funkcji i jej parametrow ponizej.

# In[ ]:

def f():
    '''Ta funkcja nie robi nic!
       
       Ta funkcja ma wyłącznie cel pedagogiczny:
       1. nie pobiera żadnych parametrów
       2. nie robi nic pożytecznego
       3. ale za to jest dobrze udokumentowana :P'''


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

