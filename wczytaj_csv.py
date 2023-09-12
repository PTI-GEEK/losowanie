import csv


def read_datas(file_name):
    ret_dict = {}
    ret_ids = []
    with open(file_name, newline='') as csvfile:
        datas = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in datas:
            game_id = row[0]
            school = row[1]
            team = f"{row[2].strip()}_{row[3].strip()}"
            download = row[4]
            downl_add = row[5]
            films = row[9]
            cart = row[11]

            ret_ids.append(game_id)
            ret_dict[game_id] = {
                "ID_GRY": game_id,
                "Zespół_Gra": team,
                "Rodzaj": school,
                "Karta": cart,
                "Pliki" : download,
                "Dod. Pliki": downl_add,
                "Film": films,
            }
    return ret_ids, ret_dict

if __name__ == "__main__":
    d = read_datas("implementacje.csv")
    print(d[1])