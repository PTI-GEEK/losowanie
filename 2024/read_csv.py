# reading CSV and writing pickle object
import pickle
import polars as pl

plik_csv = "GEEK_2024_2024-02-26_15-45.csv"
dane = pl.read_csv(plik_csv, separator=";")
print(dane.columns)
dane_small = dane[["ID", "Link", "Kategoria"]]
dane_koncepcja = dane_small.filter(pl.col("Kategoria") == "koncepcja gry")[["ID", "Link",]]
dane_implementacja = dane_small.filter(pl.col("Kategoria") == "implementacja gry")[["ID", "Link",]]

with open("dane_koncepcja.bin", "wb") as koncepcja:
    pickle.dump(dane_koncepcja, koncepcja)
    print(dane_koncepcja)
    dane_koncepcja.write_csv("koncepcja.csv")

with open("dane_implementacja.bin", "wb") as implementacja:
    pickle.dump(dane_implementacja, implementacja)
    print(dane_implementacja)
    dane_implementacja.write_csv("implementacja.csv")


dane_implementacja.iter_rows()