
# coding: utf-8

# ##pozyteczne funkcje
# funkcja <tt>'len'</tt> - liczebnosc kolekcji

# In[ ]:

li = list(range(10))
li


# In[ ]:

len(li)


# In[ ]:

len({1,2,3})


# funkcje <tt>'min/max'</tt>  - elementy skrajne

# In[ ]:

min(li), max(li)


# funkcja <tt>'sum'</tt> - suma elementów

# In[ ]:

sum(li)


# 
# ### funkcja <tt>'zip()'</tt>
# <tt>'zip()'</tt> to bardzo pozyteczna funkcja sluzaca do parowania odpowiadajacych sobie elementow sekwencji

# In[ ]:

li = list(zip(('a','b','c'), range(0,3)))
li


# In[ ]:

li = list(zip(('a','b','c', 'd'), range(1,5), range(100,110)))
li


# ponowne wywolanie <tt>'zip()'</tt> dokona 'rozpiecia' sekwencji:

# In[ ]:

li2 = list(zip(*li))
li2


# In[ ]:

len(li2)


# In[ ]:

u,v,z = li2
print(u)
print(v)
print(z)


# jednym z zastosowań funkcji <tt>'zip()'</tt> może być tworzenie słowników:

# In[ ]:

v


# In[ ]:

dict(zip(u,z))


# #Operatory i ich użycie
# operator przynaleznosci <tt>'in'</tt> sprawdza czy element nalezy do kolekcji:

# In[ ]:

'a' in u


# In[ ]:

4 not in v


# co do zasady operatory są **lewostronnie** łączne

# In[ ]:

3/3/3


# z wyjątkiem operatora <tt>'**'</tt> który jest łączny __prawostronnie__ czyli <tt>3&#42;&#42;3&#42;&#42;3</tt> jest równe  $3^{3^3}$

# In[ ]:

3**3**3


# In[ ]:

3**3**3 == 3**27


# ### 'odpakowanie' sekwencji
# operatora przypisania <tt>'='</tt> mozna uzywac w ciekawy sposob

# In[ ]:

a,b,c = range(3)


# jak widac jednym przypisaniem nadalismy wartosci 3 zmiennym

# In[ ]:

print(a,b,c)


# jest to tak zwane 'odpakowanie sekwencji'. nalezy pamietac ze liczba argumentow po obu stronach musi byc zgodna

# In[ ]:

a,b,c,d = (3,2,1) # błąd


# ## Operatory porownania

# operatory porównania w Pythonie mają ciekawe własności - mozna stosowac zapis 'matematyczny', niespotykany w innych jezykach

# In[ ]:

a = 4
3<a<5


# In[ ]:

5>a>4


# ###'rozszerzone' operatory przypisania
# Python oferuje 'rozszerzone' operatory przypisania ktorych dzialanie polega na wykonaniu operacji na lewym i prawym operandzie i przypisaniu wyniku operacji do lewego operandu. Na przyklad:

# In[ ]:

a = 6
a += 2
a


# In[ ]:

a **= 2
a


# In[ ]:

# ale uwaga na ciagi znakowe!
a = []
a += ['Ala']
a


# ###porownywanie kolekcji
# kolekcje mozna porownywac podobnie jak typy elementarne

# In[ ]:

'Ala' < 'Ola'


# In[ ]:

[1,2,4] > [1,2,3,4]


# In[ ]:

(1,2,3)>(1,2,3,4)


# In[ ]:

{'x','y','z',1,3,5} == {5,'z',3,'x','y',1}


# # Sterowanie przepływem programu

# ##pętla <tt>for</tt>
# Prosze zwrócić uwage na formatowanie kodu - **wcięcia** są elementem składni Pythona i wyznaczają granice logicznych bloków kodu:
# 
# ```python
# for zmienna in sekwencja:
#         blok kodu, który ma być powtarzany
#         dopoki sekwencja elementow sie nie wyczerpie
# else:
#         blok kodu, który ma być wykonany
#         kiedy sekwencja elementow sie wyczerpie
#         (nie zostanie wykonany jeśli w bloku 
#         poprzednim wykonamy komende 'break')
# ```
#         
# Sekcja <tt>'else'</tt> jest **opcjonalna**.

# In[ ]:

for i in range(10):
    print(i)


# In[ ]:

lista = list(range(20))
lista.reverse()
lista


# In[ ]:

for i in lista:
    a = 3
    print(i, end=' ')


# ##Instrukcja warunkowa <tt>if</tt>
# 
# Ogolna forma instrukcji warunkowej w Pythonie jest nastepująca:
# 
# ```python
# if warunek1:
#     blok kodu, który ma być wykonany
#     jeśli warunek1 jest prawdziwy
# elif warunek2:
#     blok kodu, który ma być wykonany
#     jeśli warunek2 jest prawdziwy
# elif warunek3:
#     blok kodu, który ma być wykonany
#     jeśli warunek3 jest prawdziwy
#  .
#  .
#  .
# else:
#     blok kodu, który ma być wykonany
#     jeśli każdy z powyższych warunków jest fałszywy
#       ```
# Sekcje <tt>'elif'</tt> oraz <tt>'else'</tt> sa **opcjonalne**.
# W Pythonie nie ma instrukcji <tt>'switch/case'</tt>

# In[ ]:

for i in range(10):
    if i % 2 == 0: 
        print('%i jest liczbą parzystą' % i)
    else:
        print('%i jest liczbą nieparzystą' % i)


# #### jak działa komenda 'continue'?

# In[ ]:

for i in range(10):
    if i % 2 == 0: 
        print('%s jest liczbą parzystą' % i)
        continue
    print('%s jest liczbą nieparzystą' % i)


# <H2 id="wyr_war">wyrażenia warunkowe</H2>
# uproszczoną formą instrukcji warunkowej sa *wyrażenia warunkowe*. ogólna struktura jest nstp:
# 
# ```python
# <wartość jeśli warunek spełniony> if <warunek> else <wartość w p.p.>
# ```

# In[ ]:

for i in range(10):
    print(i, 'jest liczbą', 'parzystą' if i % 2 == 0 else 'nieparzystą')


# ##pętla <tt>while</tt>
# 
#     while <warunek>:
#         blok kodu, który ma być powtarzany
#         dopóki warunek jest prawdziwy
#     else:
#         blok kodu, który ma być wykonany
#         kiedy warunek jest fałszywy
#         (nie zostanie wykonany jeśli w bloku 
#         poprzednim wykonamy komende 'break')
#         
# Sekcja <tt>'else'</tt> jest **opcjonalna**.

# In[ ]:

# przyklad: znajdz 'tajemnicza' liczbe
liczba = 23
ile_prob = 6

while 3>2:
    strzal = int(input('Wpisz liczbę całkowitą: '))
    if strzal == liczba:
        print('Gratulacje! Zgadłeś tajemniczą liczbę: ', liczba)
        break
    elif strzal < liczba:
        print('Szukana liczba jest większa od podanej. Próbuj dalej')
    else:
        print('Szukana liczba jest mniejsza od podanej. Próbuj dalej')
    ile_prob -= 1
else:
    print('Niestety, nie odgadles tajemniczej liczby :(')
print('Koniec programu')


# In[ ]:

int(input('podaj liczbe:'))


# ## Sekwencje 'sklejane'
# 
# Szczególną forma pętli <tt>for</tt> sa tzw sekwencje sklejane albo składane (ang. *list comprehensions*). Jest to bardzo przydatne i wygodne narzedzie.
# Przyjmijmy ze chce policzyc kwadraty pewnego ciagu liczb. Moge to zrobic tak

# In[ ]:

kwadraty = []
for n in range(10):
    kwadraty.append(n**2)

kwadraty


# ale istnieje wygodniejszy sposob:

# In[ ]:

[x**2 for x in range(10)]


# chce wyznaczyc iloczyn kartezjanski zbiorow A i B

# In[ ]:

A = set(range(5))
B = {'a', 'b', 'c'}
print(A,B)


# moge tak:

# In[ ]:

C = []
for a in A:
    for b in B:
        C.append((a,b))
C


# ale mozna prosciej :-)

# In[ ]:

[(a,b) for a in A for b in B]


# moge tez uzyc klauzuli <tt>if</tt> zeby wyrzucic elementy 'diagonalne':

# In[ ]:

A = tuple(range(5))
A


# In[ ]:

list( (a,b) for a in A for b in A if a != b)


# a gdybym chcial policzyc sumę elementow z dwoch kolekcji moge to zrobic tak:

# In[ ]:

A = list(range(10))
B = list(range(9,0,-1))
A,B


# In[ ]:

print(*zip(A,B))


# In[ ]:

[a+b for a,b in zip(A,B)]


# In[ ]:

z = input("wprowadź liczbę:")


# In[ ]:

type(z)


# ## Zad. 1.1
# Oblicz średnią wektora $\mathbf{v}$

# In[ ]:

v = list(range(10))


# ## Zad. 1.2
# Przeanalizuj poniższy kod. Zmień jego działanie w taki sposób, aby w wyswietlanym rezultacie znak '*' został zastąpiony przez odpowiednia cyfrę, np '7' dla drugiej pozycji liczby 173.
# 
# **UWAGA** chodzi o zmiane kodu programu, a nie definicji elementów listy 'Cyfry'

# In[ ]:

Zero = ["  ***  ", " *   * ", "*     *", "*     *", "*     *",
        " *   * ", "  ***  "]
One = [" * ", "** ", " * ", " * ", " * ", " * ", "***"]
Two = [" *** ", "*   *", "*  * ", "  *  ", " *   ", "*    ", "*****"]
Three = [" *** ", "*   *", "    *", "  ** ", "    *", "*   *", " *** "]
Four = ["   *  ", "  **  ", " * *  ", "*  *  ", "******", "   *  ",
        "   *  "]
Five = ["*****", "*    ", "*    ", " *** ", "    *", "*   *", " *** "]
Six = [" *** ", "*    ", "*    ", "**** ", "*   *", "*   *", " *** "]
Seven = ["*****", "    *", "   * ", "  *  ", " *   ", "*    ", "*    "]
Eight = [" *** ", "*   *", "*   *", " *** ", "*   *", "*   *", " *** "]
Nine = [" *** ", "*   *", "*   *", " ****", "    *", "    *", " *** "]

Cyfry = [Zero, One, Two, Three, Four, Five, Six, Seven, Eight, Nine]

liczba = input("wprowadź liczbę:")
row = 0
while row < 7:
    line = ""
    column = 0
    while column < len(liczba):
        number = int(liczba[column])
        cyfra = Cyfry[number]
        line += cyfra[row] + "  "
        column += 1
    print(line)
    row += 1


# In[ ]:

S = 'Ala ma kota'


# In[ ]:

S[0] = 'O'


# In[ ]:

'aaaaaaba'.replace('a','*')


# In[ ]:

li = ['Ala', 'Ola', 'Ula']


# In[ ]:

li[2].replace('a','*')


# In[ ]:

[S.replace('a','*') for S in li]

