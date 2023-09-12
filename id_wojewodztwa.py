import csv, pickle


def read_datas(file_name):
    ret_dict = {}
    ret_ids = []
    with open(file_name, newline='') as csvfile:
        datas = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in datas:
            game_id = row[5]
            category = row[2]
            location = row[0]
            school_type = row[6]
            name = row[7]
            mail = row[8]
            phone = row[9]
            datas_g = f"{row[3]}_{row[4]}"
            print(f"{category=}")
          
            ret_dict[game_id] = [ location, category, school_type, name, mail, phone, datas_g ]
            
    return ret_dict

if __name__ == "__main__":
    d = read_datas("id_all_short.csv")
    with open("id_all.bin", 'wb') as pf:
        pickle.dump(d, pf)
