# Bulls and Cows
Jest to prosta gra dla dwóch osób, której celem jest znalezienie przez gracza A kodu wymyślonego przez gracza B.

## Przebieg gry
- gracz B wymyśla kod będący liczbą (najczęściej 4-cyfrową), w której każda cyfra jest inna
- gracz A zgaduje liczbę
- gracz B zwraca dwie wartości liczbowe: "bulls" i "cows" oznaczające kolejno ile poprawnych cyfr na odpowiednich pozycjach i ile poprawnych cyfr na nieodpowiednich pozycjach udało się graczowi A zgadnąć
- gracz A kontynuuje zgadywanie do czasu zgadnięcia poprawnej liczby (po której zwrócona zostanie odpowiedź bulls=4 cows=0)

## Przykładowa rozgrywka
| Guess | Response |
| --- | --- |
| 1234 | bulls=0 cows=1 |
| 5678 | bulls=0 cows=1 |
| 9012 | bulls=1 cows=1 |
| 9087 | bulls=1 cows=1 |
| 1087 | bulls=0 cows=1 |
| 9205 | bulls=3 cows=0 |
| 9305 | bulls=4 cows=0 |

# Dane wejściowe
liczba jaką należy zgadnąć

# Dane wyjściowe
lista zgadnięć
