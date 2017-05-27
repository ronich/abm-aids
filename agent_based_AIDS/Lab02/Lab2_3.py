
# coding: utf-8

# # Zajęcia 2 c.d.

# ##Programowanie obiektowe
# Programowanie obiektowe (ang. _object-oriented programming_) jest najpopularniejszą obecnie techniką tworzenia programów komputerowych. W tym podejściu program komputerowy wyraża się jako zbiór _obiektów_, które są bytami łączącymi stan (opisany przez _atrybuty_) i zachowanie (_metody_, które są procesami operującymi na atrybutach). W celu realizacji zadania obliczeniowego obiekty wywołują nawzajem swoje metody, zlecając w ten sposób innym obiektom odpowiedzialność za wybrane działania. 
# 
# Opakowanie razem logicznie powiązanych danych i procesów nazywamy _kapsułkowaniem_ (ang. _encapsulation_). W porównaniu z tradycyjnym programowaniem proceduralnym, w którym dane i procedury nie są ze sobą powiązane, programowanie obiektowe ułatwia zrozumienie, konserwację i rozwój kodu programu. W konsekwencji ułatwia tworzenie dużych systemów informatycznych i współpracę wielu programistów. Modularność kodu obiektowego pozwala też na ponowne wykorzystywanie istniejącego kodu. 
# 
# Największym atutem programowania obiektowego jest zbliżenie programów komputerowych do ludzkiego sposobu postrzegania rzeczywistości. Czasami nazywa się to zmniejszeniem luki reprezentacji (ang. _representational gap_). Dlatego ludzie są w stanie łatwiej zapanować nad kodem i tworzyć większe programy. Łatwiej jest również zrozumieć kod i pomysły innych programistów i tym samym współpracować w zespole oraz ponownie wykorzystywać istniejące rozwiązania. Co więcej tego naturalnego sposobu myślenia i tych samych pojęć można użyć zarówno w trakcie analizy i dekompozycji problemu jak i w trakcie projektowania jego programowego rozwiązania. Jest to szczególnie użyteczne w kontekście modelowania wieloagentowego, w którym agentów określonego typu możemy reprezentować bezpośrednio jako *obiekty* określonej *klasy*.
# 
# Warto wiedzieć, że koncepcja programowania obiektowego zrodziła się z potrzeby tworzenia złożonych symulacji. Pierwszy język obiektowy [Simula 67](http://en.wikipedia.org/wiki/Simula) powstał już w latach sześćdziesiątych ubiegłego stulecia. Jego twórcami byli Ole-Johan Dahl i Kristen Nygaard z Norsk Regnesentral w Oslo. Podczas prac nad symulacją portu handlowego musieli dla każdego rodzaju statku uwzględniać wiele zmiennych. Ponieważ liczba modelowanych rodzajów statków była duża, uwzględnienie wszystkich możliwych zależności między atrybutami stało się problematyczne. Pojawił się pomysł, aby reprezentować statki jako egzemplarze określonego typu/klasy. Każda klasa statków była opisana przez atrybuty i zachowania. [zobacz animacje](http://wazniak.mimuw.edu.pl/images/c/cd/Statki.swf)

# **Klasa** i **obiekt** to podstawowe pojęcia w programowaniu obiektowym i należy je starannie odróżniać.
# Klasyfikacja, czyli łączenie występujących w rzeczywistości obiektów w jednorodne grupy – klasy, jest najbardziej naturalnym sposobem rozumienia rzeczywistości. Klasa obejmuje zbiór obiektów o podobnej strukturze i właściwościach i jednoznacznie określa ich **typ**. Użyteczną analogią jest relacja pojęć gatunek i osobnik, w której poszczególne osobniki odpowiadają _obiektom klasy_ Gatunek.
# ### 'wszystko jest obiektem'
# Klasę możemy również rozumieć jako wyspecjalizowany typ danych. Poznaliśmy podstawowe typy danych Pythona takie jak liczby całkowite, zmiennoprzecinkowe i zespolone oraz krotki czyli n-tki uporządkowane. Pomimo ich elementarnej natury również one są klasami posiadającymi specyficzną strukturę i właściwości. Na przykład liczby zespolone mają dwie składowe (atrybuty) - rzeczywistą i urojoną, a dla obiektu klasy 'krotka' możemy określić liczebność i porządek ciągu elementów. 
# 
# Dzięki programowaniu obiektowemu możemy definiować własne, bardziej złożone lub wyspecjalizowane, typy danych opisujące strukturę i własności obiektów, które chcemy modelować. Na przykład możemy zdefiniować klasę <tt>'Prostokat'</tt> która będzie posiadała atrybuty <tt>'długość'</tt> i <tt>'szerokość'</tt> oraz metodę <tt>'powierzchnia()'</tt> obliczającą pole jego powierzchni.
# W Pythonie i innych językach obiektowych klasa pełni role **matrycy** służącej do tworzenia obiektów określonego typu. Używając klasy <tt>Prostokat</tt> możemy zatem zdefiniować obiekty <tt>f1</tt> i <tt>f2</tt> reprezentujące odrębne figury o różnych wymiarach.

# In[ ]:

class Prostokat:
    '''klasa reprezentuje prostokąt w wymiarach dlug x szer'''
    
    # metoda __init__ to metoda specjalna
    # służąca do inicjalizacji obiektu (konstruktor)
    # wywoływana jest automatycznie 
    # kiedy tworzymy obiekt danej klasy
    def __init__(self, dlug, szer):
        self.dlug = dlug
        self.szer = szer


# In[ ]:

# tworzymy zmienna (obiekt) typu Prostokat
# Python wywoła 'w tle' metodę __init__()
f1 = Prostokat(10,12)
type(f1)


# In[ ]:

f1


# In[ ]:

class Prostokat:
    '''klasa reprezentuje prostokąt w wymiarach dlug x szer'''
    
    # metoda __init__ to metoda specjalna
    # służąca do inicjalizacji obiektu (konstruktor)
    # wywoływana jest automatycznie 
    # kiedy tworzymy obiekt danej klasy
    def __init__(self, dlug, szer):
        self.dlug = dlug
        self.szer = szer
     
    def powierzchnia(self):
        '''oblicza pole powierzchni prostokąta'''
        return self.dlug * self.szer


# In[ ]:

# tworzymy zmienna (obiekt) typu Prostokat
# Python wywoła 'w tle' metodę __init__()
f1 = Prostokat(10,12)
type(f1)


# In[ ]:

# wywolujemy metode obiektu
f1.powierzchnia()


# In[ ]:

print(f1)


# In[ ]:

class Prostokat:
    '''klasa reprezentuje prostokąt w wymiarach dlug x szer'''
    
    # metoda __init__ to metoda specjalna
    # służąca do inicjalizacji obiektu (konstruktor)
    # wywoływana jest automatycznie 
    # kiedy tworzymy obiekt danej klasy
    def __init__(self, dlug, szer):
        self.dlug = dlug
        self.szer = szer
    
    # metoda __repr__ to metoda specjalna
    # która zwraca opis obiektu
    # w formie wywołania pozwalającego
    # na stworzenie jego duplikatu
    def __repr__(self):
        return 'Prostokat({},{})'.format(self.dlug, self.szer)
    
    # kolejna metoda specjalna
    # wywolywana automatycznie 
    # kiedy obiekt tej klasy przekażemy 
    # jako argument dla funkcji 'print'
    def __str__(self):
        return 'jestem Prostokat od wymiarach {} x {}'.format(self.dlug, self.szer)
      
    def powierzchnia(self):
        '''oblicza pole powierzchni prostokąta'''
        return self.dlug * self.szer


# In[ ]:

# tworzymy zmienna (obiekt) typu Prostokat
f2 = Prostokat(5,11)
f2.powierzchnia()


# In[ ]:

print(f2)


# In[ ]:

f2.dlug


# Kolejną ważna koncepcja w programowaniu obiektowym jest **dziedziczenie**. Jest to mechanizm pozwalajacy na tworzenie wyspecjalizowanych typów danych (klas potomnych) na bazie typów bardziej ogólnych (klas bazowych). Poniżej definiujemy klasę <tt>Kwadrat</tt> będącą 'potomkiem' klasy <tt>Prostokat</tt>. Jak widać nawę klasy bazowej podajemy w nawiasie po nazwie tworzonej klasy potomnej (jeśli nie podamy nazwy klasy bazowej tworzona klasa dziedziczy domyślnie po klasie <tt>object</tt>, która jest 'korzeniem' drzewa hierarchii klas w Pythonie).
# 
# Warto wspomnieć, że możliwe jest dziedziczenie po kilku klasach bazowych, choć nie będziemy korzystać z tej możliwości. Osoby zainteresowanie odsyłam do [dokumentacji](http://docs.python.org/3.4/tutorial/classes.html#multiple-inheritance).

# In[ ]:

# klasa Kwadrat jest klasą potomną
# klasy Prostokat
class Kwadrat(Prostokat):
    def __init__(self, bok):
        super().__init__(bok, bok)


# In[ ]:

# tworzymy obiekt typu Kwadrat
f3 = Kwadrat(10)


# In[ ]:

f3


# Zaletą mechanizmu dziedziczenia jest to, iż nie musimy ponownie implementować tych fragmentów kodu, które sa wspólne dla bazowej i potomnej klasy. Klasa  '<tt>Kwadrat</tt>'  nie zawiera implementacji metody  '<tt>powierzchnia()</tt>', ale mozemy ja wywołać, gdyż została _odziedziczona_ po klasie bazowej '<tt>Prostokat</tt>'.

# In[ ]:

# wywolujemy metode obiektu
f3.powierzchnia()


# metoda `mro()` wyswietla hierarchię dziedziczenia klasy:

# In[ ]:

Kwadrat.mro()


# In[ ]:

type(f1), type(f2), type(f3)


# polecenie `isinstance` sprawdza, czy obiekt jest _instancją_ wskazanej klasy:

# In[ ]:

isinstance(f2, Prostokat)


# In[ ]:

isinstance(f2, Kwadrat)


# In[ ]:

isinstance(f3, Kwadrat)


# In[ ]:

isinstance(f3, Prostokat)


# poleceniem `subclass` sprawdzamy, czy Klasa1 jest podklasa Klasy2:

# In[ ]:

issubclass(Kwadrat, Prostokat)


# In[ ]:

issubclass(Prostokat, Kwadrat)


# Metoda '`mro()`' zwraca hierarchie dziedziczenia dla danej klasy. Korzeniem hierarchii klas jest klasa '`object`'. Przedrostek `__main__` wskazuje ze klasy '`Kwadrat`' i '`Prostokat`' zostaly zdefiniowane w _globalnej_ przestrzeni nazw.

# In[ ]:

Kwadrat.mro()


# okazuje sie, ze w Pythonie nawet elementarne typy danych sa klasami:

# In[ ]:

int.mro(), str.mro(), list.mro()


# ###Obiekt jako 'pojemnik' na dane
# Obiekty możemy traktować jak 'uniwersalny' pojemnik na dane:

# In[ ]:

class Pojemnik:
    pass


# In[ ]:

poj = Pojemnik()
poj


# In[ ]:

type(poj)


# In[ ]:

poj.a = 10
poj.b = 100
poj.c = 'Akuku'


# In[ ]:

poj.a = 12
poj.a


# In[ ]:

del poj.b


# In[ ]:

f1.wys


# In[ ]:

f1.szer, f1.dlug


# In[ ]:

f1.wys = 10


# In[ ]:

f1.szer, f1.dlug, f1.wys


# In[ ]:

f1.powierzchnia()


# In[ ]:

f1.szer = 5
f1.powierzchnia()


# In[ ]:

del f1.dlug


# In[ ]:

f1.powierzchnia()

