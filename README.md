[![Codacy Badge](https://app.codacy.com/project/badge/Grade/1ad4ebea0b3b43fd9f2d9efac4d27f94)](https://www.codacy.com/gh/suchencjusz/Bombunia/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=suchencjusz/Bombunia&amp;utm_campaign=Badge_Grade)
# Bombunia
Program sprwadza co określony interwał oceny klasy,
porównuje ich ilość z poprzednim sprawdzaniem, po sprawdzeniu
wysyła je na serwer discord

Projekt ciągle rozwijany, aktualnie jego kod jest co najmniej *żenujący*

## TODO:
- [ ] Ogarnięcie samego działania programu (działa jakby chciał a nie mógł),
- [ ] Łapanie błędów json'a (chodzi o sprwadzenie pliku ```cookies.json```),
- [ ] Stworzenie pliku konfiguracyjnego ```setup.py```,
- [ ] Webhooki discorda,
- [ ] Ogarnięcie nazw funkcji i zmiennych, takich jak ```MuchiosAmogisGrades``` lub ```dupa```,
- [ ] Stworzenie systemu zapisu ocen i porównywania ich (tak jak w [Bombeczka](https://github.com/suchencjusz/Bombeczka)).

# Instalacja

```
git clone https://github.com/suchencjusz/Bombunia
cd Bombunia
pip -r requirements.txt
python setup.py
```

Przeglądarka dla selenium
- [Firefox](https://github.com/mozilla/geckodriver/releases) 