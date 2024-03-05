import pickle
import json
import polars as pl
from random import choice

plik_csv = "GEEK_2024_2024-03-05_22-50.csv"
circles_count = 35

podzial_gier = {}
przydzielone = {}

def get_game_id(iids, old_games, count=3):
    if not iids:
        return -1
    ret = False
    counted = 0
    rid = -1
    while not ret:
        counted += 1
        rid = choice(iids)
        try:
            if przydzielone[rid] == 3:
                # print(f"{counted=} / {rid=}")
                # print(f"{rid=} : {przydzielone[rid]=}")
                # old_games.append(rid)
                return -1
        except:
            pass
        if rid in old_games:
            if counted < count:
                continue
            else:
                return -1
        ret = True

    return rid


# wczytanie danych z CSV
dane = pl.read_csv(plik_csv, separator=";", ignore_errors=True)
print(dane.columns)
# dane_sent = dane.filter(pl.col("Status") == "Wysłane")[["ID", "Link", "Kategoria"]]
dane_sent = dane.filter(pl.col("Status") == "Wysłane")[["ID", "Link", "Kategoria"]]
print(dane_sent)
dane_sent.write_excel('dane_wyslane.xls')
dane_koncepcja = dane_sent.filter(pl.col("Kategoria") == "koncepcja gry")[["ID", "Link", ]]
dane_implementacja = dane_sent.filter(pl.col("Kategoria") == "implementacja gry")[["ID", "Link", ]]

with open("dane_koncepcja.bin", "wb") as koncepcja:
    pickle.dump(dane_koncepcja, koncepcja)
    print(dane_koncepcja)
    dane_koncepcja.write_csv("koncepcja.csv")

with open("dane_implementacja.bin", "wb") as implementacja:
    pickle.dump(dane_implementacja, implementacja)
    print(dane_implementacja)
    dane_implementacja.write_csv("implementacja.csv")

# przetwarzanie danych
with open("dane_koncepcja.bin", "rb") as koncepcja:
    dane_koncepcja = {}
    dane_kon = pickle.load(koncepcja)
    for id, data in dane_kon.iter_rows():
        dane_koncepcja[id] = data
    id_koncepcji = list(dane_koncepcja.keys())

with open("dane_implementacja.bin", "rb") as implementacja:
    dane_implementacja = {}
    dane_kon = pickle.load(implementacja)
    for id, data in dane_kon.iter_rows():
        dane_implementacja[id] = data
    id_implementacji = list(dane_implementacja.keys())

testers = ('PD', 'TC', 'AM', 'AW', 'JK', 'MT', 'AS', 'EA', 'MK', 'TK')
testy_konc = {}
testy_impl = {}

for initials in testers:
    testy_konc[initials] = []
    testy_impl[initials] = []

for circle in range(circles_count):
    for tester in testers:
        games_done_k = testy_konc[tester]
        games_done_i = testy_impl[tester]
        print(f"{tester=} / {testy_konc[tester]=}")
        id_k = get_game_id(id_koncepcji, games_done_k, count=(circle * 3) + 10)
        print(f"{tester=} / {testy_impl[tester]=}")
        id_i = get_game_id(id_implementacji, games_done_i, count=(circle * 3) + 10)
        if id_k > 0:
            testy_konc[tester].append(id_k)
            if not id_k in podzial_gier:
                podzial_gier[id_k] = ["Koncepcja"]
            podzial_gier[id_k].append(tester)
            if not id_k in przydzielone:
                przydzielone[id_k] = 0
            przydzielone[id_k] += 1

        if id_i > 0:
            testy_impl[tester].append(id_i)
            if not id_i in podzial_gier:
                podzial_gier[id_i] = ["Implementacja"]
            podzial_gier[id_i].append(tester)
            if not id_i in przydzielone:
                przydzielone[id_i] = 0
            przydzielone[id_i] += 1

# dane output
for tester in testers:
    file_name = f"juror_{tester}.xlsx"
    ids = testy_konc[tester]
    rodzk = ["Koncepcja" for _ in range(len(ids))]
    idi = testy_impl[tester]
    rodzi = ["Implementacja" for _ in range(len(idi))]
    links = [dane_koncepcja[id_k] for id_k in ids]
    linki = [dane_implementacja[id_i] for id_i in idi]
    dane_do_df = {
        "RODZAJ": rodzk + rodzi,
        "ID_GRY": ids + idi,
        "LINK_WWW": links + linki,
    }
    df_k = pl.DataFrame(dane_do_df)
    df_k.write_excel(file_name)

with open("podzial_gier.json", "w") as pgier:
    json.dump(podzial_gier, pgier, ensure_ascii=True, indent= 3)

ile_gier = 0
zbyt_malo = 0
for gra in podzial_gier:
    ile_gier += 1
    ile_przydzielono = len(podzial_gier[gra])

    if ile_przydzielono < 4:
        zbyt_malo += 1
        print(f"Uwaga: {gra=} => {podzial_gier[gra]=}")
    else:
        print(f"OK: {gra=} => {ile_przydzielono=}")
else:
    print(f"Koniec sprawdzenia przydziału gier dla: {ile_gier=} / {zbyt_malo=}")
    print(przydzielone)