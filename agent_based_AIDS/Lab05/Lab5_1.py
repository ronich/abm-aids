
# coding: utf-8

# # Zajęcia 5

# ## [Biblioteka standardowa c.d.](http://docs.python.org/3.4/library/index.html)

# ###decimal
# 
# moduł do operacji na liczbach zmiennoprzecinkowych o podstawie dziesiętnej - rozwiązuje problemy z precyzją obliczeń o których mówiliśmy na pierwszych ćwiczeniach. Przykład praktyczny - obliczamy podatek VAT 5% od kwoty netto 0.7 PLN:

# In[91]:

net_amnt = 0.7
vat_rate = 0.05
tax_amnt = net_amnt * vat_rate
tax_amnt


# In[92]:

gross = net_amnt + tax_amnt
gross


# w wyniku zaokraglenia otrzymanej liczby otrzymujemy _błędny_ wynik (np. niezgodny z ustawa o VAT):

# In[93]:

round(gross,2)


# te same operacje z wykorzystaniem typu <tt>Decimal</tt> (prosze zwrocic uwage ze wartosci przekazujemy jako ciagi znakowe - co by sie stalo gdybysmy przekazali je w postaci liczb zmiennoprzecinkowych <tt>float</tt>?):

# In[94]:

# importujemy klase Decimal z modułu decimal do globalnej przestrzeni nazw
from decimal import Decimal


# In[95]:

net_amnt = Decimal('.7')
vat_rate = Decimal('0.05')
tax_amnt = net_amnt * vat_rate
tax_amnt


# In[96]:

net_amnt


# In[97]:

gross = net_amnt + tax_amnt
gross


# teraz wynik jest _poprawny_ (i zgodny z ustawa VAT):

# In[98]:

round(gross,2)


# ## [praca z plikami](http://docs.python.org/3.4/tutorial/inputoutput.html#reading-and-writing-files)

# otwarcie pliku do zapisu:

# In[99]:

f = open('plik_1.txt', 'w')


# In[100]:

import os


# In[101]:

os.getcwd()


# In[ ]:

os.chdir('C:\\')


# In[102]:

get_ipython().system('ls')


# In[103]:

f.write('Ala ma kota')


# In[104]:

f.write('Ola ma psa')


# In[105]:

# plik jest pusty...
get_ipython().system('cat plik_1.txt')


# In[106]:

f.close()


# In[107]:

# plik juz nie jest pusty!
get_ipython().system('cat plik_1.txt')


# otwarcie pliku do zapisu:

# In[108]:

f = open('plik_1.txt', 'w')


# In[109]:

# plik znowu jest pusty!
# (otwarcie do zapisa czysci plik)
get_ipython().system('cat plik_1.txt')


# In[110]:

f.write('Ala ma kota\n')


# In[111]:

# plik jest pusty
get_ipython().system('cat plik_1.txt')


# In[112]:

f.flush()


# In[113]:

# plik juz nie jest pusty!
get_ipython().system('cat plik_1.txt')


# In[114]:

f.write('Ola ma psa\n')


# In[115]:

f.writelines('Ula i Ela')


# In[116]:

# Ola jest w buforze...
get_ipython().system('cat plik_1.txt')


# In[117]:

f.close()


# In[118]:

# Ola jest w pliku!
get_ipython().system('cat plik_1.txt')


# jesli wystapi blad - mozemy utracic niezapisane informacje

# In[119]:

f = open('plik_1.txt', 'w')
f.write('Ala ma kota\n')
f.write('Ola ma psa\n')
f.read() # błąd! plik nie otwarty do odczytu
f.close()


# In[120]:

get_ipython().system('cat plik_1.txt')


# <tt>try/except/finally</tt> - jesli wystapi blad, _nie_ utracimy niezapisanych informacji:

# In[121]:

try:
    f = open('plik_1.txt', 'w')
    f.write('Ala ma kota\n')
    f.write('Ola ma psa\n')
    f.read()
except Exception as e:
    print('Wystapil błąd:', e)
finally:
    f.close()


# In[122]:

get_ipython().system('cat plik_1.txt')


# prostsza forma tego co wyzej:

# In[123]:

with open('plik_1.txt', 'a') as f:
    f.write('Ala ma kota\n')
    f.write('Ola ma psa\n')
    f.read()
print(data)


# In[ ]:

get_ipython().system('cat plik_1.txt')


# In[124]:

# otwarcie pliku do odczytu
with open('plik_1.txt', 'r') as f:
    data = f.read()
print(data)


# In[125]:

#otwarcie pliku do odczytu
with open('plik_1.txt', 'r') as f:
    data = f.readlines()
print(data)


# In[126]:

# otwarcie pliku do odczytu
with open('plik_1.txt', 'r') as f:
    i = 0
    for line in f:
        i += 1
        print(i, line, end='')


# ### `csv`
# moduł [csv](http://docs.python.org/3.4/library/csv.html) jest częścią biblioteki standardowej i jak nietrudno sie domyslić służy do odczytu i zapisu plików w formacie .csv

# In[127]:

import csv


# In[128]:

with open('eggs.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Spam'] * 5 + ['Baked Beans'] + [5])
    writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'] + [1,2,3])
    writer.writerow(range(10))


# In[129]:

get_ipython().system('cat eggs.csv')


# In[130]:

with open('eggs.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)


# flaga <tt>csv.QUOTE_NONNUMERIC</tt> powoduje, ze pola numeryczne beda automatycznie konwertowane do postaci <tt>float</tt>:

# In[131]:

with open('eggs.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(['Spam'] * 5 + ['Baked Beans'] + [5])
    writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'] + [1,2,3])


# In[132]:

get_ipython().system('cat eggs.csv')


# In[133]:

with open('eggs.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        print(row)

