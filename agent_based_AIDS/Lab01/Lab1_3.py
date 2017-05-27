
# coding: utf-8

# # Złożone typy danych (kolekcje)
# Podstawowe typy złożone (kolekcje) to *krotki, listy, zbiory i slowniki*. Dwa pierwsze typy przechowuja elementy w sposob uporzadkowany - kazdemu elementowi przypisany jest unikalny indeks $i \in \{0,\ldots,n-1\}$ gdzie $n \in \mathbb{N}$ jest liczebnością kolekcji (dlatego alternatywnie typy te sa nazywane *ciągami* lub *sekwencjami*). Pozwala to na dostep do wskazanych elementow jak do elementow tablicy. Zbiory i slowniki nie przechowuja elementow w okreslonej kolejnosci, ale gwarantuja *unikalnosc* elementow.

# ## krotki (tuple)

# Najprosztszym złożonym typem danych w Pythonie sa *krotki* czyli n-tki uporządkowane.
# Krotki przechowują uporządkowane ciągi elementów *dowolnego typu*. Elementy nie muszą być unikalne.

# In[ ]:

(1,2,4,4, '4')


# mozemy pominac nawiasy kiedy typ danych wynika jasno z kontekstu:

# In[ ]:

n=1,2,5,4
n


# In[ ]:

type(n)


# ale w przypadkach niejednoznacznych trzeba uzywac nawiasow

# In[ ]:

type(1,2,5,4) # błąd!


# In[ ]:

type((1,2,5,4))


# aby utworzyc krotke jednoelementowa uzywamy składni:

# In[ ]:

type((1,))


# lub

# In[ ]:

1.,


# podobnie jak ciągi znaków krotki mozna konkatenowac

# In[ ]:

(1,2,5,4) + ('a',3.) + (3,)


# In[ ]:

# oraz powielac
n=(1,2,5,4)*3
n


# In[ ]:

# ale nie mozna modyfikowac elementow krotki po jej utworzeniu
n[1]=3


# Krotki sa prostszym typem danych niz lista i oferuja tylko dwie metody:

# In[ ]:

help(tuple.count)
help(tuple.index)


# ## listy (lists)
# Pdobnie jak krotki, **listy** przechowywuja uporządkowane ciągi elementów *dowolnego typu*. Listę tworzymy uzywająć nawiasow kwadratowych. Listy moga zawierac powtarzajace sie elementy.

# In[ ]:

[1,2,4,4]


# Listy mozna tworzyc w kilku liniach. Moga zawierac elementy roznych typow

# In[ ]:

n = [ 1,
3.4,
'hello',
True,
2-1J, (1,2,3)]


# In[ ]:

n


# Listy indeksujemy podobnie jak ciagi znakow. 1-szy element ma indeks 0

# In[ ]:

n[1]


# element ostatni ma indeks -1

# In[ ]:

n[2:-1]


# dla elementów 'zagniezdzonych' mozemy uzywac notacji jak dla tablic wielowymiarowych:

# In[ ]:

n[-1][1:]


# podobie jak ciagi znakow listy mozna konkatenowac

# In[ ]:

n + [3, 4, 'pięć']


# oraz powielać

# In[ ]:

n = [1,2,3,5] * 2
n


# w odrożnieniu od krotek zawartosc listy **mozemy modyfikowac**:

# In[ ]:

n = [1,2,3,'blah']
n


# In[ ]:

n[3]=4
n


# In[ ]:

n += 5,
n


# In[ ]:

n += [0]
n


# listy mozna sortowac w porzadku rosnacym

# In[ ]:

n.sort()
n


# lub malejacym

# In[ ]:

n.sort(reverse=True)
n


# mozna tez odwrocic kolejnosc elementow

# In[ ]:

n.reverse()
n


# In[ ]:

help(list)


# mozna sumowac elementy listy

# In[ ]:

sum(n)


# wybierac elementy skrajne

# In[ ]:

min(n), max(n)


# pod warunkiem ze typy elemetow sa zgodne

# In[ ]:

n.append('name2')
n


# Listy możemy używać jako *kolejek*.
# Do wrzucania elementow na koniec kolejki sluzy metoda <tt>'append':</tt>

# In[ ]:

n.append(1)
n.append('Ala')
n.append(4.234)
n


# Przykład kolejki LIFO (taka struktura danych jest tez nazywana *stosem*) 
# -- do pobrania ostatnio wrzuconego elementu uzywamy metody <tt>'pop()':</tt>

# In[ ]:

x = n.pop()
print("pobrano:", x, " w kolejce pozostalo", len(n), "elementów:", n)


# Przykład kolejki FIFO -- do pobierania najstarszego wrzuconego elementu uzywamy wywolania <tt>'pop(0)':</tt>

# In[ ]:

n.append(222)


# In[ ]:

n


# In[ ]:

x = n.pop(0)
print("pobrano:", x, " w kolejce pozostalo", len(n), "elementów:", n)


# mozemy tworzyc listy z wykorzystaniem *generatorow* (jak funkcja <tt>range()</tt>):

# In[ ]:

n=list(range(2,11))
n


# mozemy usuwac elementy listy wskazujac ich indeksy

# In[ ]:

del(n[3])
n


# lub wartosci

# In[ ]:

n.remove(10)
n


# wycinanie fragmetu listy (*slicing*):

# In[ ]:

n[3:5]


# wstawianie listy dowolnego rozmiaru w srodek innej listy:

# In[ ]:

n[3:5]=['A','B','C', 'D']
n


# Mozna zadac pytanie po co nam krotki skoro listy oferuja to co krotki i wiele wiecej? Gospodarka pamiecia w przypadku krotek jest znacznie bardziej oszczedna niz w przypadku list. Jesli nie musisz modyfikowac zestawu danych -  do jego przechowania **uzywaj krotek**!

# ##zbiory (sets)
# zbiory to proste kolekcje przechowujace elementy dowolnego typu ktorych kolejnosc jest nieistotna

# In[ ]:

z = {'Ola', 5.2, 'Ala', 'Ela'}
z


# elementów zbioru nie mozemy indeksowac poniewaz ich kolejnosc jest nieokreslona:

# In[ ]:

z[1]


# elementy zbioru mozna usuwac

# In[ ]:

z.remove(5.2)
z


# elementy mozna dodawac

# In[ ]:

z.add('Ula')
z


# elementy zbioru sa unikalne:

# In[ ]:

z.add('Ala')
z


# Python wspiera następujące działania na zbiorach:
# 
# <table class="wikitable" border="1">
# <tbody>
# <tr>
# <th>
# <br>
# </th>
# <th>Operator
# </th>
# <th>Nazwa
# </th>
# <th>Wyjaśnienie
# </th>
# <th>Przykłady
# </th>
# </tr>
# <tr>
# <td rowspan="10" style="background-color:#d3f9d3"
# align="center"> o<br>
# p<br>
# e<br>
# r<br>
# c<br>
# j<br>
# e<br>
# <br>
# n<br>
# a<br>
# <br>
# z<br>
# b<br>
# i<br>
# o<br>
# r<br>
# a<br>
# c<br>
# h
# </td>
# <td align="center"> |
# </td>
# <td> Suma zbiorów
# </td>
# <td> Zwraca zbiór wszystkich elementów które są w
# pierwszym zbiorze lub są w drugim zbiorze.
# </td>
# <td> <tt>set([1,3,5]) | set([7,3])</tt> daje <tt>set([1,3,5,7])</tt>.
# </td>
# </tr>
# <tr>
# <td align="center"> −
# </td>
# <td> Różnica zbiorów
# </td>
# <td> Zwraca zbiór elementów które są w pierwszym
# zbiorze i nie są w drugim zbiorze.
# </td>
# <td> <tt>set([1,3,5]) − set([7,3])</tt> daje <tt>set([1,5])</tt>.
# </td>
# </tr>
# <tr>
# <td align="center"> &amp;
# </td>
# <td> Przecięcie (część wspólna, iloczyn) zbiorów
# </td>
# <td> Zwraca zbiór elementów które są w pierwszym
# zbiorze i są w drugim zbiorze.
# </td>
# <td> <tt>set([1,3,5]) &amp; set([7,3])</tt> daje <tt>set([3])</tt>.
# </td>
# </tr>
# <tr>
# <td align="center"> ^
# </td>
# <td> Elementy unikalne
# </td>
# <td> Zwraca zbiór zawierający elementy nie będące
# wspólne dla dwu zbiorów.
# </td>
# <td> <tt>set([1,3,5]) ^ set([7,3])</tt> daje <tt>set([1,5,7])</tt>.
# </td>
# </tr>
# <tr>
# <td align="center"> in
# </td>
# <td> Sprawdzenie czy jest elementem.
# </td>
# <td> Zwraca wartość logiczną zdania „x jest elementem
# zbioru A”.
# </td>
# <td> <tt>3 in set([1,3,5])</tt> daje <tt>True</tt>.
# </td>
# </tr>
# <tr>
# <td align="center"> not in
# </td>
# <td> Sprawdzenie czy nie jest elementem
# </td>
# <td> Zwraca wartość logiczną zdania „x nie jest
# elementem zbioru A”.
# </td>
# <td> <tt>3 not in set([1,3,5])</tt> daje <tt>False</tt>.
# </td>
# </tr>
# <tr>
# <td align="center"> &lt;
# </td>
# <td> Sprawdzenie czy jest podzbiorem
# </td>
# <td> Zwraca wartość logiczną zdania „A jest podzbiorem
# zbioru B”.
# </td>
# <td> <tt>set([1,3]) &lt; set([7,3])</tt> daje <tt>False</tt>.<br>
# <tt>set([1,3]) &lt; set([1,7,3])</tt> daje <tt>True</tt>.
# </td>
# </tr>
# <tr>
# <td align="center"> &gt;
# </td>
# <td> Sprawdzenie czy jest nadzbiorem
# </td>
# <td> Zwraca wartość logiczną zdania „A jest nadzbiorem
# zbioru B”.
# </td>
# <td> <tt>set([1,5,3]) &gt; set([7,3])</tt> daje <tt>False</tt>.<br>
# <tt>set([1,5,3]) &gt; set([1,3])</tt> daje <tt>True</tt>.
# </td>
# </tr>
# <tr>
# <td align="center"> ==
# </td>
# <td> Sprawdzenie czy są jednakowe
# </td>
# <td> Zwraca wartość logiczną twierdzenia, że każdy
# element pierwszego zbioru jest elementem drugiego
# zbioru i każdy element drugiego zbioru jest
# elementem pierwszego.
# </td>
# <td> <tt>set([1,3,5]) == set([7,3])</tt> daje <tt>False</tt>.<br>
# <tt>set([1,3,5]) == set([5,3,1])</tt> daje <tt>True</tt>.
# </td>
# </tr>
# <tr>
# <td align="center">&nbsp;!=
# </td>
# <td> Sprawdzenie czy nie są jednakowe
# </td>
# <td> Zwraca wartość logiczną twierdzenia, że pierwszy
# zbiór nie jest jednakowy z drugim.
# </td>
# <td> <tt>set([1,3,5])&nbsp;!= set([7,3])</tt> daje <tt>True</tt>.
# </td>
# </tr>
# </tbody>
# </table>
# 

# przyklady:

# In[ ]:

y = {'Ela', 'Ala', 'Ania'}
print('zbior y: ', y, '\nzbior z: ', z)


# In[ ]:

# suma
y | z


# In[ ]:

# czesc wspolna
y & z


# In[ ]:

# czy 'Ala' jest elementem zbioru y?
'Ala' in y


# ##słowniki (dict)
# Słowniki sa implementacją tzw. *tablic asocjacyjnych*. Przechowuja one mapowania <tt>'klucz:wartosc'</tt>. Klucze sa unikalne. Kluczem moze byc dowolny obiekt **niemodyfikowalnego** typu danych czyli liczba, string, krotka.

# In[ ]:

s = {'Sty':1, 'Lut':2, 'Mar':3, 'Kwie':4, 'Maj':5, '???':13}
s


# In[ ]:

type(s)


# ze slownika mozemy pobierac wartosc wg klucza:

# In[ ]:

s[1]


# In[ ]:

s['Maj']


# In[ ]:

s.get('Kwie')


# In[ ]:

# wstawiac nowe wartosci do slownika
s['Cze']=6
s


# In[ ]:

# zamieniac wartosci istniejacych kluczy
s['Kwie']=4
s.get('Kwie')


# In[ ]:

# oraz usuwac klucze
del s['???']
s

