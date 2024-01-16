# reading CSV and writing pickle object
import csv
import pickle
import polars as pl


dane = pl.read_csv("dane.csv", separator=";")
print(dane)
print(dane.describe())
print(dane.columns)
print(dane["Status"])