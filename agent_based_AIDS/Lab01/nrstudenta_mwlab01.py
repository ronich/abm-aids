# ## Zad. 1.1
# Oblicz średnią wektora v

v = list(range(10))


# ## Zad. 1.2
# Przeanalizuj poniższy kod. Zmień jego działanie w taki sposób, aby w wyswietlanym rezultacie znak '*' został zastąpiony przez odpowiednia cyfrę, np '7' dla drugiej pozycji liczby 173.
# **UWAGA** chodzi o zmiane kodu programu, a nie definicji elementów listy 'Cyfry'

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

