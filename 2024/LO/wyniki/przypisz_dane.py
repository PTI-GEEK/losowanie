import pandas as pd
import csv

plik_dane = "/home/adasiek/my_projects/PTI/losowanie/2024/wojew.xlsx"
dane_csv = "/home/adasiek/my_projects/PTI/losowanie/2024/wojew.csv"
plik_juror = "00_LO_Wyniki.xlsx"

woj = {}
with open(dane_csv, "r") as csvf:
    for line in csvf:
        id, nazwa = line.split(",")
        woj[int(id)] = nazwa.strip()

dane_kon = pd.read_excel(plik_juror, sheet_name="KONCEPCJA", engine="openpyxl")
dane_imp = pd.read_excel(plik_juror, sheet_name="IMPLEMENTACJA", engine="openpyxl")


# for elem in dane_kon["ID GRY"]:
#      id_gry = int(elem)
#      wojewodztwo = woj[id_gry]
#      koncepcje = dane_kon.with_columns(funkcja((pl.col("ID GRY"))).alias("WWW"))

def funkcja(idgry):
    return woj[int(idgry)]

# dane_kon["WOJ"] = "None"
# dane_kon["WOJ"].apply(funkcja(dane_kon["ID GRY"]))
dane_kon.to_csv("tmp.csv", index=False)

output = []
with open("tmp.csv", "r") as csvf:
    for line in csvf:
        dane_linia = line.strip().split(",")
        try:
            dane_int = [int(x) for x in dane_linia]
            idgry = int(dane_int[0])
            dane_int.append(funkcja(idgry))
            output.append(dane_int)
        except:
            print(f"Error -> {dane_linia}")
            dane_int = [x for x in dane_linia]
            dane_int.append("WOJ")
            output.append(dane_int)
            pass

print(output)
with open("00_LO_Wyniki_woj.csv", "w") as csvf:
    writer = csv.writer(csvf)
    for line in output:
        print(line)
        writer.writerow(line)