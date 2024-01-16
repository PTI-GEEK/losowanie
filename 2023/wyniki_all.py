import csv, pickle, json


def read_datas(file_name):
    with open("id_all.bin", 'rb') as pf:
        games = pickle.load(pf)
        
    ret_dict = {}
    ret_woj = {}
    ret_ids = []
    all_data = []
    with open(file_name, newline='') as csvfile:
        datas = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in datas:
            game_id = row[0]
            points = float(row[1].replace(",","."))
            location, category, school_type, name, mail, phone, datas_g = games[game_id]
            all_data.append([game_id, points, location, category, school_type, datas_g, name, mail, phone])
            idx = f"{location.lower()}_{school_type.lower()}_{category.lower()}"
            # print(idx, game_id, points)
            # ret_dict[game_id] = [ location, category, school_type ]
            if not idx in ret_woj:
                ret_woj[idx] = {}

            ret_woj[idx][game_id] = points
            # ret_dict[game_id] = points
            
            
        all_sorted = {}
        for element in ret_woj:
            sorted_dict = dict(sorted(ret_woj[element].items(), reverse=True, key=lambda x: x[1]))
            all_sorted[element] = sorted_dict
            
    return ret_woj, all_sorted, all_data

if __name__ == "__main__":
    d, s, a = read_datas("id_oceny.csv")
    print(a)
    header = ["game_id", "points", "location", "category", "school_type", "datas_g", "name", "mail", "phone"]
    with open("wyniki.csv", 'w') as csvfile: 
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerows(a)

    # print(s)
    with open("wyniki_posortowane.txt", "w") as jsw:
        json.dump(s, jsw, ensure_ascii=False, indent=3)
        

