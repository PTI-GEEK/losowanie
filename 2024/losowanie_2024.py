import pickle
import polars as pl
from random import choice

circles_count = 5


def get_game_id(ids, old_games, count=3):
    if not ids:
        return -1
    ret = False
    counted = 0
    while not ret:
        counted += 1
        rid = choice(ids)
        if rid in old_games:
            if counted < count:
                continue
            else:
                return -1
        ret = True

    return rid


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

testers = {
    "PD": "pawel.dymora@prz.edu.pl",
    "TC": "tcichocka@gazeta.pl",
    "AM": "a.mowna@issi.uz.zgora.pl",
    "AW": "awrzeciono@interia.pl",
    "JK": "jkaczor@nowodworek.krakow.pl",
    "MT": "mtokarz.zsem@gmail.com",
    "AS": "a.stolinska@gmail.com",
    "EA": "ewa.ankiewicz-jasinska@o2.pl",
    "MK": "maciej.kazon@inzynierowie.com",
}

testy_konc = {}
testy_impl = {}

for initials in testers.keys():
    testy_konc[initials] = []
    testy_impl[initials] = []

for circle in range(circles_count):
    for tester in testers.keys():
        games_done_k = testy_konc[tester]
        games_done_i = testy_impl[tester]
        id_k = get_game_id(id_koncepcji, games_done_k, count=(circle * 2) + 3)
        id_i = get_game_id(id_implementacji, games_done_i, count=(circle * 2) + 3)
        if id_k > 0:
            testy_konc[tester].append(id_k)
        if id_i > 0:
            testy_impl[tester].append(id_i)


# dane output
for tester in testers.keys():
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
