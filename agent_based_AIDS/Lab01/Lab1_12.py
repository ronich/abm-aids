
# coding: utf-8

# #Dlaczego Python?
# Python jest prostym i łatwym do opanowania językiem programowania ogólnego zastosowania. Przejrzyste reguły składni powodują, że kod napisany w Pythonie ma czytelną strukturę. 
# Python jest językiem coraz częściej wybieranym przez środowisko naukowe do [obliczeń numerycznych](http://scipy.org) i [analizy danych](http://pydata.org). Dzięki jego popularności w tej dziedzinie zastosowań istnieje bogaty ekosystem gotowych do użycia bibliotek programistycznych wykonujących typowe zadania, bez potrzeby pisania tych fragmentów kodu samemu. 
# 
# Python jest oprogramowaniem otwartego źródła (ang. *open source*) i jest dostępny nieodpłatnie dla wszystkich popularnych systemów operacyjnych.

# ## Praca z Pythonem
# 
# Python jest językiem interpretowanym. Dzięki temu mamy dwie możliwości wykonywania programu
# + interaktywnie - w linii poleceń, Python wykonuje komendy 'na bieżąco'
# + wsadowo - zapisując polecenia w pliku tekstowym i wykonując je jako program

# # 1. Elementarne typy danych

# ##1.1 Typy numeryczne
# W Pythonie zdefiniowano trzy liczbowe typy danych: 
# + całkowite (ang. integers), 
# + zmiennoprzecinkowe (ang. floating point albo krócej: float)
# + zespolone (ang. complex).

# ###liczby całkowite (int):
# W trybie interaktywnym Pythona mozna uzywac jak kalkulatora. Prosty przyklad - w linii komend Pythona wprowadzamy

# In[ ]:

5+7


# W wiekszosci jezyków programowania liczby calkowite (integer) sa zapisywane w pamieci komputera przy uzyciu 4 lub 8 bajtow. Ogranicza to zakres wartosci ktore mozna przedstawic do odpowiednio $\{0,\ldots,2^{32}\}$ i $\{0,\ldots,2^{64}\}$ dla liczb nieujemnych. Natomiast w Pythonie jedynym ograniczeniem wartości liczb całkowitych jest pojemność pamięci operacyjnej komputera

# In[ ]:

2**3264


# Operator <tt>'**'</tt> jest w Pythonie operatorem potegowania (<tt>'^'</tt> jest natomiast operatorem bitowej roznicy symetrycznej, XOR).

# ###liczby zmiennoprzecinkowe (float):
# dla odróżnienia od liczb calkowitych liczbe zmiennoprzecinkową uzupełniamy kropka dziesietna

# In[ ]:

123.456


# pominiecie wartosci przed lub po kropce przyjmuje wartosc domyslna '0'

# In[ ]:

1.


# In[ ]:

.23


# W wersji 3. Pythona wynik operacji dzielenia jest zawsze liczbą zmiennoprzecinkową (w Pythonie v2 wynikiem dzielenia dwoch liczb calkowitych jest liczba calkowita, nawet jesli wynik jest liczba niecałkowita)

# In[ ]:

3/1


# In[ ]:

3/3


# W odroznieniu od liczb calkowitych zakres liczb zmiennoprzecinkowych w Pythonie (i nie tylko!) jest ograniczony. Wynika to ze sposobu reprezentacji tych liczb w pamieci komputera.

# In[ ]:

2.**1023


# In[ ]:

2.**1024


# In[ ]:

2.**-1074


# In[ ]:

2.**-1075


# ####Dygresja - czy komputery naprawdę się nie mylą?
# Podobnie jak zakres ograniczona jest rownież precyzja obliczen na liczbach zmiennoprzecinkowych. Aby to zilustrowac wykorzystamy operator '==' bedacy w Pythonie operatorem rownosci. Zaczniemy od sprawdzenia trywialnej tozsamosci:

# In[ ]:

.3 == .3


# Jesli powyzsze jest prawdziwe to prawdziwe jest tez:

# In[ ]:

.3 == (3 * .1)


# Skad ten zakakujacy (i błędny) wynik?! spojrzmy:

# In[ ]:

3 * .1


# In[ ]:

.7*.05


# Powyzszy rezultat nie swiadczy o bledzie w Pythonie ale jest 'wlasnoscia' arytmetyki zmiennoprzecinkowej wspolczesnych komputerow opartej na systemie binarnym, w którym nie można w precyzyjny sposób przedstawić ułamków dziesiętnych.
# Podobne niespojnosci powstaja kiedy w dzialaniach arytmetycznych operujemy na liczbach zmiennoprzecinkowych odleglych o wiele rzedow wielkosci:

# In[ ]:

10.0**16 + 3 - 10.0**16


# W 'typowych' zastosowaniach takie niescislosci nie zaburzaja uzyskanych wynikow, jednak warto byc swiadomym ograniczen arytmetyki zmiennoprzecinkowej wspolczesnych komputerow. Osobom szerzej zainteresowanym tym tematem polecam tę [stronę](http://osilek.mimuw.edu.pl/index.php?title=MN03).

# ### liczby zespolone (complex):
# Python pozwala tez na prowadzenie obliczen na liczbach zespolonych

# In[ ]:

1+3j


# In[ ]:

type(-2J)


# Dla poprawnosci dzialan liczby zespolone ujmyjemy w nawiasy

# In[ ]:

3-1j*3+5j  #  niepoprawny zapis błędny wynik!


# In[ ]:

# a tak jest dobrze
(3-1j)*(3+5j)


# zakres liczb zespolonych jest ograniczony podobnie jak liczb zmiennoprzecinkowych

# In[ ]:

(2-2j)**683


# ###wartości logiczne (bool)
# W Pythonie wartosci 'prawda' i 'fałsz' sa w reprezentowane przez słowa kluczowe <tt>'True'</tt> i <tt>'False'</tt>

# In[ ]:

True


# In[ ]:

False


# In[ ]:

type(True)


# In[ ]:

type(False)


# Kiedy używamy operatorów poównania (<tt>==</tt>, <tt>!=</tt>, <tt>&lt;=</tt>, <tt>&gt;=</tt>, <tt>&lt;</tt>, <tt>&gt;</tt>), w wyniku otrzymujemy jedną z dwóch wartości logicznych <tt>True</tt>&#160;/&#160;<tt>False</tt>.
# Większość innych wyrażeń nie jest prawdziwa lub fałszywa w sensie matematycznym. Na przykład napis <tt>"Hello, World"</tt> nie ma wartości logicznej w sensie matematycznym.
# Niemniej w Pythonie, jak też w wielu innych językach programowania, wszystkie obiekty mają wartość logiczną określaną zgodnie z pewnymi ustalonymi regułami. Pozwala to wykorzystać dowolne wyrażenie jako warunek w poleceniu sterujących wykonaniem programu, jak <tt>if</tt> czy <tt>while</tt>, bo każde wyrażenie zwraca jakiś obiekt.
# W przypadku obiektów które nie są po prostu <tt>True</tt> ani <tt>False</tt>,
# to czy dany obiekt zostanie zinterpretowany jako prawdziwy, czy też jako fałszywy, rządzi się paroma prostymi regułami:
# </p>
# <ol><li> w przypadku liczb, liczba 0 jest fałszywa, wszystkie pozostałe są prawdziwe
# </li><li> w przypadku sekwencji (np. napisów) i innych kolekcji, tylko te puste, o długości 0, są fałszywe
# </li><li> pozostałe obiekty są prawdziwe (o ile ich twórca nie podjął specjalnych działań by mogły mieć różne wartości logiczne)
# </li></ol>
# 

# Funkcja <tt>bool()</tt> sluzy do przeksztalcania wartosci dowolnego wyrazenia na wartosc logiczna. Zgodnie z zasadami przedstawionymi powyzej wartosci reprezentujace '0' lub zbior pusty przeksztalcane sa na wartosc <tt>False</tt>, pozostale na <tt>True</tt>. Moze to prowadzic do niespodziewanych wynikow

# In[ ]:

# nalezy zwracac uwage na wielkosc liter w slowach kluczowych
bool(True)


# In[ ]:

bool('False')


# In[ ]:

bool('')


# In[ ]:

bool(1)


# In[ ]:

bool(0)


# In[ ]:

bool(-1)


# In[ ]:

bool(0.000000000000000000000000000000000000000000001)


# In[ ]:

bool(0+0j)


# In[ ]:

bool(1-0j)


# In[ ]:

bool(0+.1j)


# Standardowe dzialania algebry Boola sa reprezentowane przez operatory <tt>'and' 'or' i 'not'</tt>

# In[ ]:

True and False


# In[ ]:

not False


# In[ ]:

False or True


# ##1.2 Ciągi znakowe (str)
# Kolejnym elementarnym typem danych są napisy (ciągi tekstowe). Napisy ograniczamy pojedynczym ...

# In[ ]:

'Hello world'


# ... lub podwójnym cudzysłowem

# In[ ]:

"Hello world"


# ale musimy zachowac konsekwencje

# In[ ]:

"Hello world' # błąd!


# ciagi tekstowe mozemy sklejać przy uzyciu operatora konkatenacji '+'

# In[ ]:

"Hello " + 'world'


# albo tak:

# In[ ]:

"Hello " 'world'


# ciągi można powielać przy uzyciu operatora <tt>'*'</tt>

# In[ ]:

3 * 'Hello world! '


# ciąg tekstu moze miec wiele linii

# In[ ]:

'Ala ma kota i psa'


# In[ ]:

print("Ala ma kota, psa i papugę")


# mozemy tez uzyc potrójny cudzysłów
# pamietajac ze w miejscu lamania wiersza wstawia on znak konca linii <tt>'\n'</tt>
# 

# In[ ]:

'''Ala ma kota
i psa'''


# In[ ]:

print("""Ala ma kota,
psa
i papugę""")


# znak nowej linii czasami sprawia klopoty

# In[ ]:

print('C:\some\name')  # here \n means newline!


# wtedy mozemy posilkowac sie flaga <tt>'r'</tt> ktora powoduje ignorowanie symboli specjalnych w tekscie

# In[ ]:

print(r'C:\some\name')  # note the r before the quote


# # 2. Zmienne

# W Pythonie zmienna to identyfikator alfanumeryczny wskazujacy na jakas wartosc (a dokladnie na 'obiekt' - to pojecie omowimy wkrotce). Python używa dynamicznego typowania zmiennych, co oznacza iż:
# 1. zmiennych nie trzeba deklarowac
# - zmienne 'powołujemy' do życia przez przypisanie wartosci do nazwy symbolicznej uzywajac operatora przypisania <tt>'='</tt>
# - typ zmiennej jest okreslony przez typ wartosci do niej przypisanej w trakcie wykonania programu
# 
# ### Nazewnictwo identyfikatorów
# Tworząc identyfikatory w Pythonie, musimy trzymać się kilku zasad:
# Pierwszym znakiem identyfikatora musi być mała lub wielka litera alfabetu łacińskiego (więc polskie znaki są niedopuszczalne) albo podkreślnik (<tt>_</tt>).
# - Pozostałe znaki mogą zawierać małe lub wielkie litery alfabetu łacińskiego, podkreślniki oraz cyfry (<tt>0</tt>-<tt>9</tt>).
# - Wielkość znaków w identyfikatorze jest ważna. Stąd <tt>mojanazwa</tt> i <tt>mojaNazwa</tt> to zupełnie co innego. Zwróć uwagę na wielkie <tt>N</tt> w drugim przykładzie.
# - Przykłady <i>poprawnych</i> identyfikatorów to: <tt>i</tt>, <tt>__moja_nazwa</tt>, <tt>nazwa_23</tt>, <tt>a1b2_c3</tt>.
# - Przykłady <i>niepoprawnych</i> identyfikatorów to: <tt>2nazwy</tt>, <tt>nazwa ze spacjami</tt>, <tt>moja-nazwa</tt>.
# * nazwy zmiennych nie moga sie pokrywac ze slowami kluczowymi Pythona

# In[ ]:

n = 5


# In[ ]:

n


# In[ ]:

# polecenie 'type' zwraca typ (klase - rowniez to pojecie omowimy wkrotce) obiektu przypisanego do zmiennej
type(n)


# In[ ]:

n=5.
n


# In[ ]:

type(n)


# In[ ]:

n = 'Ala ma kota'
n


# In[ ]:

type(n)


# In[ ]:

# błąd! nazwy zmiennych nie moga sie pokrywac ze slowami kluczowymi Pythona
or = 5


# ## 1.2 Ciągi znakowe C.D.

# ciągi tekstowe można indeksować jak tablice

# In[ ]:

# ściągawka:
# +---+---+---+---+---+---+
# | P | y | t | h | o | n |
# +---+---+---+---+---+---+
#   0   1   2   3   4   5 
#  -6  -5  -4  -3  -2  -1

n = 'Python'
n[0]


# In[ ]:

n[-1]


# In[ ]:

# mozemy tez podac zakres elementow ciągu uzywajac notacji [od:do]
n[0:3]


# In[ ]:

# wartoscia domyslna indeksu 'od' jest 0
n[:3]


# In[ ]:

# a indeksu 'do' -1
n[1:]


# In[ ]:

# wobec tego ponizszy zapis zwroci wszystkie elementy ciagu
n[:]


# ###nie mozemy bezposrednio modyfikowac zawartosci ciagu tekstowego

# In[ ]:

n[0]='E'  # błąd! ciągi tekstowe są niemodyfikowalne!


# ale ciągi można konkatenować (sklejać) przy pomocy operatora `+`

# In[ ]:

n + ' is a snake'


# oraz 'powielać' operatorem `*`

# In[ ]:

n * 3


# Istnieje wiele uzytecznych *metod* ktore oferuje obiekt typu 'str' (czym jest 'obiekt' i 'metoda' wyjaśnimy bardziej szczegółowo na kolejnych zajeciach). Kilka przykladow ponizej:

# In[ ]:

n.upper()


# In[ ]:

n.lower()


# In[ ]:

n = 'Ala ma kota'
n.split()


# W trybie interaktywnym pełną listę metod możemy uzyska korzystajac z polecenia <tt>'help'</tt>. Metody ktorych nazwy zaczynaja sie i kończą '__' to metody 'specjalne' Pythona. Co do zasady metody specjalne sa przeznaczone dla interpretera Pythona a nie dla uzytkownika koncowego
# ale nie ma mechanizmu 'blokujacego' dostep do nich. W pewnych sytuacjach (jak sie przekonamy na kolejnych spotkaniach) ich bezposrednie uzycie moze byc pozyteczne.
# 

# In[ ]:

help(str)

