
# coding: utf-8

# # Zajęcia 4 cz.2

# ##Obsługa wyjątków
# Wyjątek to błąd który powstaje _w trakcie działania programu_ (dla odrożnieniena od błędów ktory popełniamy w trakcie pisania kodu).

# In[ ]:

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

# In[ ]:

while True:
    try:
        liczba = int(input("Podaj liczbę: "))
        print("10 podzielone przez", liczba, "równa się", 10/liczba)
    except (ZeroDivisionError) as e:
        print(e, ': nie dzielimy przez zero!')
    except (ValueError) as e:
        print(e, ': zly format liczby')


# Istotna jest kolejnosc klauzul except. Na poczatku wyłapujemy wyjątki najbardziej szczegołowe, w dalszej kolejnosci bardziej ogólne. W ustaleniu własciwej kolejności pomocna jest [hierarchia wyjątków](http://docs.python.org/3/library/exceptions.html#exception-hierarchy)

# In[ ]:

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


# In[ ]:

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

# In[ ]:

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

# In[ ]:

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

# In[ ]:



