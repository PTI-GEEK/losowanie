import json

file_sp = "podzial_gier_szkola_podstawowa.json"
file_lo = "podzial_gier_szkola_ponadpodstawowa.json"
fsp_konc_tak = "sp_konc_tak.csv"
fsp_konc_nie = "sp_konc_nie.csv"
fsp_impl_tak = "sp_impl_tak.csv"
fsp_impl_nie = "sp_impl_nie.csv"

def spr(game_testers, all_testers):
    for one in game_testers:
        if one in all_testers:
            return (True, one)
    return (False, "NN")

# SP
testers_sp = ('PD', 'AW')
# LO
testers_lo = ('MT', 'AS', 'TK')

with open(file_sp, "r") as fsp:
    dane_sp = json.load(fsp)

with open(file_lo, "r") as flo:
    dane_lo = json.load(flo)

print("--- [Podstawowa] ----------")
for idgry in dane_sp:
    rodzaj, testerzy = dane_sp[idgry][0],dane_sp[idgry][1:]
    spr_ok, who = spr(testerzy, testers_sp)
    if spr_ok:
        print("OK", idgry, rodzaj, testerzy, who)
    else:
        print("NOT ---> ", idgry, rodzaj, testerzy, who)

print("--- [Liceum] ----------")

for idgry in dane_lo:
    rodzaj, testerzy = dane_lo[idgry][0],dane_lo[idgry][1:]
    spr_ok, who = spr(testerzy, testers_lo)
    if spr_ok:
        print("OK", idgry, rodzaj, testerzy, who)
    else:
        print("NOT ----->", idgry, rodzaj, testerzy, who)