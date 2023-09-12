import pickle
import json
from random import choice
from wczytaj_csv import *

file_name = "koncepcje"
# file_name = "implementacje"

id_gry, dane_gier = read_datas(f"{file_name}.csv")
# id_gry = [n for n in range(1,82)]

win_only = (19,21,29,36,47,51,54,67,80,69,70,71,75,77,78,81)
len_win_only = len(win_only)
set_win_only = set(win_only)


def get_game_id(ids, old_games, not_games = False):
    if not ids:
        return -1
    ret = False
    # rid = None
    while not ret:
        # print(f"{ids=}")
        rid = choice(ids)
        if rid in old_games:
            # continue
            return -1
        # print(f"{id=}")
        if not_games:
            if len(ids) == len_win_only:
                if set(ids) == set_win_only:
                    return -1
            if rid not in win_only:
                ret = True
        else:
            ret = True
    return rid


testers = (
    "Paweł Dymora",
    "Wojciech Kolarz",
    "Agnieszka Marekwia-Wójcik",
    "Hanna Pikus",
    "Tomasz Żmijewski",
    "Rafał Kołodziejczyk",
    "Bogdan Malisz",
    "Anna Wrzeciono",
    "Wiesław Grządziel",
    "Monika Szkiel-Mnich",
    "Karolina Antkowiak",
    "Adam Jurkiewicz",
    "Dawid Pindel",
    "Krzysztof Kielak",
)

sprawdzenia = {
    0: {
        "gry": None,
        "tester": [0,1,2],
    },

    1: {
        "gry": None,
        "tester": [0, 1, 2],
    },

    2: {
        "gry": None,
        "tester": [0, 1, 2],
    },


}


for sprawdzenie in sprawdzenia:
    sprawdzenia[sprawdzenie]["gry"] = id_gry.copy()

    for tid in testers:
        sprawdzenia[sprawdzenie][tid] = []

    while sprawdzenia[sprawdzenie]["gry"]:
        for tid in testers:
            if tid == "Adam Jurkiewicz":
                if sprawdzenie == 0:
                    id_game = get_game_id(sprawdzenia[sprawdzenie]["gry"],[], True)
                elif sprawdzenie == 1:
                    spr_gry = sprawdzenia[0][tid]
                    id_game = get_game_id(sprawdzenia[sprawdzenie]["gry"], spr_gry , True)
                elif sprawdzenie == 2:
                    old = sprawdzenia[0]["gry"] + sprawdzenia[1]["gry"]
                    id_game = get_game_id(sprawdzenia[sprawdzenie]["gry"], sprawdzenia[0]["gry"] + sprawdzenia[1]["gry"], True)

                if id_game == -1:
                    break
            else:
                if sprawdzenie == 0:
                    id_game = get_game_id(sprawdzenia[sprawdzenie]["gry"], [])
                elif sprawdzenie == 1:
                    id_game = get_game_id(sprawdzenia[sprawdzenie]["gry"], sprawdzenia[0]["gry"])
                elif sprawdzenie == 2:
                    id_game = get_game_id(sprawdzenia[sprawdzenie]["gry"], sprawdzenia[0]["gry"] + sprawdzenia[1]["gry"])
                if id_game == -1:
                    break
            idx = sprawdzenia[sprawdzenie]["gry"].index(id_game)
            sprawdzenia[sprawdzenie]["gry"].pop(idx)
            # print(f"TID: {tid} -> gra {id_game}")
            sprawdzenia[sprawdzenie][tid].append(id_game)

    else:
        for tid in testers:
            print(f"{sprawdzenie=} / {tid=}")
            print(sprawdzenia[sprawdzenie][tid])


with open(f"{file_name}.dat", "wb") as pfile:
    pickle.dump(sprawdzenia, pfile)

with open(f"{file_name}.json", "w") as jfile:
    jfile.write(json.dumps(sprawdzenia,indent=3))

games_for_tester = {}
for tester_name in testers:
    games_for_tester[tester_name] = []
    for id_spr in (0, 1, 2):
        games_for_tester[tester_name] += sprawdzenia[id_spr][tester_name]


# dumper.dump(dane_gier)
# dumper.dump(games_for_tester)

games_for_tester_desc = {}

for tester_name_key in games_for_tester:
    games_ids = games_for_tester[tester_name_key]
    games_desc = [dane_gier[id_game] for id_game in games_ids]
    games_for_tester_desc[tester_name_key] = games_desc

for tester_name_key in games_for_tester:
    with open(f"{file_name}_{tester_name_key}_desc.txt", "w") as jfile:
        jfile.write(json.dumps(games_for_tester_desc[tester_name_key],indent=3, ensure_ascii=False))
