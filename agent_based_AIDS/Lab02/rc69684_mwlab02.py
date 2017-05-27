# Zadania są do zrobienia do 21.10

# In[ ]:

# coding: utf-8

# # Zadania

# ## Zad. 2.1
# Zaimplementuj funkcję **`mean(v)`** która obliczy wartość średnią sekwencji (wektora) $\mathbf{v}$.

# In[ ]:

def mean(v):
    return sum(v)/len(v)


# In[ ]:

assert mean(range(10)) == 4.5, "Błędna wartość!"
mean(range(10))


# ## Zad. 2.2
# Zaimplementuj funkcję **`stdev(v)`** która obliczy odchylenie standardowe sekwencji (wektora) $\mathbf{v}$.

# In[ ]:

def stdev(v):
    std_el = [abs(i - mean(v))**2 for i in v]
    std = mean(std_el)**(1/2)
    return std

# In[ ]:

assert abs(stdev(range(10))-2.8722813232690143) < 1e-9, "Błędna wartość!"
stdev(range(10))


# ## Zad. 2.3
# Zaimplementuj funkcję **`prod(u,v)`** która obliczy iloczyn Schura (odpowiadających sobie elementów) wektorów $\mathbf{u},\mathbf{v}$. Wynik powinien byc zwrocony jako lista.

# In[ ]:

def prod(u,v):
    schur = [i*j for i,j in zip(u,v)]
    return schur

# In[ ]:

assert list(prod(range(5), reversed(range(5)))) == [0, 3, 4, 3, 0], "Błędna wartość!"
prod(range(10), (range(10)))


# ## Zad. 2.4
# Zaimplementuj funkcję **`dot_prod(u,v)`** która obliczy iloczyn skalarny $\mathbf{u}^{T}\mathbf{v}$ podanych wektorów (sekwencji).

# In[ ]:

def dot_prod(u,v):
        prod = sum([i*j for i,j in zip(u,v)])
        return prod

# In[ ]:

assert dot_prod(range(10), (range(10))) == 285, "Błędna wartość!"
dot_prod(range(10), (range(10)))


# ##Zad. 2.5
# Napisz funkcje **`fib(n)`** ktora zwroci listę zawierającą kolejne wyrazy [ciągu Fibonacciego](http://pl.wikipedia.org/wiki/Ci%C4%85g_Fibonacciego) $\leq n$

# In[ ]:

def fib(n):
    fib_seq = [0, 1]
    if n <= 1:
        return fib_seq[:n+1]
    elif n > 1:
        while fib_seq[len(fib_seq)-1] <= n:
            fib_seq.append(fib_seq[len(fib_seq)-1]+fib_seq[len(fib_seq)-2])
        return fib_seq[:-1]

# In[ ]:

assert fib(100) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89], "Błędna wartość!"
fib(100)


# ##Zad. 2.6
# Funkcję z Zad. 6 zamień na generator

# In[ ]:

def fibgen(n):
    fib_seq = [0, 1]
    if n <= 1:
        yield fib_seq[:n+1]
    elif n > 1:
        while fib_seq[len(fib_seq)-1] <= n:
            fib_seq.append(fib_seq[len(fib_seq)-1]+fib_seq[len(fib_seq)-2])
        yield fib_seq[:-1]

