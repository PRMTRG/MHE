# Quadratic assignment problem
Mając:

- listę (rozmiaru n) lokacji, pomiędzy którymi są określone odległości
- listę (rozmiaru n) obiektów, pomiedzy którymi są określone wartości przepływu

chcemy w taki sposób umieścić w każdej lokacji jeden obiekt, aby uzyskać jak najmniejszą sumę wartości dystansów pomnożonych przez wartości przepływu występujące pomiędzy każdą z lokacji.

# Dane wejściowe
- lista lokacji
- odległości pomiędzy parami lokacji
- lista obiektów
- wartości przepływu pomiędzy parami obiektów

# Dane wyjściowe
- lista reprezentująca rozmieszczenie obiektów w lokacjach
(np. [2, 0, 1, 3] oznaczające, że na lokacji o indeksie 0 umieszczony jest obiekt o indeksie 2, na lokacji 1 obiekt 0, itd.)
