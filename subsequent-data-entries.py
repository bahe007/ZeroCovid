"""Speichert jeden Tag für die letzten zehn Tage, wie viele
Neuinfektionen nachgemeldet wurden und wie viele bereits seit
gestern bekannt waren. 
"""
import helpers

import matplotlib.pyplot as plt
import numpy as np
import csv
import datetime

file_name = helpers.todays_filename()
helpers.download_todays_data_if_needed()

t = helpers.generate_t(file_name)[-10:]

old = np.zeros(len(t)) # Datum bereits seit gestern bekannt
new = np.zeros(len(t)) # Datum in diesem Bericht neu
removed = np.zeros(len(t)) # Datum wurde in diesem Bericht entfernt

caseNumberIdx = 0
dateIdx = 0
newCaseIdx = 0

with open(file_name, "r") as fp: 
    csv_reader = csv.reader(fp, delimiter=',')

    title_row_read = False
    for row in csv_reader:
        if not title_row_read:
            caseNumberIdx = row.index("AnzahlFall")
            dateIdx = row.index("Meldedatum")
            newCaseIdx = row.index("NeuerFall")
            title_row_read = True
            continue

        caseNumber = float(row[caseNumberIdx])
        date = row[dateIdx][:-9]
        newCase = row[newCaseIdx]

        try:
            idx = t.index(date)
        except:
            continue

        if newCase == "0":
            old[idx] += caseNumber
        elif newCase == "1":
            new[idx] += caseNumber
        else:
            removed[idx] += caseNumber

# Daten abspeichern
with open("subsequent-data-entries/data.txt", "a") as f:
    f.write(datetime.datetime.now().strftime("%d-%m-%Y")+"\n")
    oldString = ""
    newString = ""
    rmvString = ""
    for i in range(len(t)):
        oldString += "{} ".format(int(old[i]))
        newString += "{} ".format(int(new[i]))
        rmvString += "{} ".format(int(removed[i]))

    f.write(oldString+"\n")
    f.write(newString+"\n")
    f.write(rmvString+"\n")
    f.write("\n")