# Data Source: https://www.arcgis.com/home/item.html?id=f10774f1c63e40168479a1feb6c7ca74

import csv
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import helpers
import case_numbers

############## Rohdaten ##############
file_name = helpers.todays_filename()
helpers.download_todays_data_if_needed()

############## Fallzahlen je Landkreis ermitteln ##############
t, counties, cases_per_county = case_numbers.get_cases_per_county(file_name)

# Sortiere nach Zahl der 0-day-Tage
zeroDaysPerCounty = dict()
for county, cases in  cases_per_county.items():
    zeroDaysPerCounty[county] = np.sum(cases == 0)
zeroDaysPerCounty = dict(sorted(zeroDaysPerCounty.items(), key=lambda item: item[1]))

# 2D-Matrix mit den täglichen Fallzahlen in einer Zeile
matrix = np.array([np.log(helpers.moving_average(cases_per_county[county])[:-3]+1)/np.log(10) for county in zeroDaysPerCounty.keys()])

############## Darstellung ##############

fig, ax = plt.subplots()
ax.set_ylabel("Landkreise")

xtick_positions = [t.index("2020/02/01"), t.index("2020/04/01"), t.index("2020/06/01"), t.index("2020/08/01"), t.index("2020/10/01"), t.index("2020/12/01")]
xlabels = ["1. Februar", "1. April", "1. Juni", "1. August", "1. Oktober", "01. Dezember"]

cax = ax.matshow(matrix, cmap=matplotlib.cm.Reds)

ax.set_xticks(xtick_positions)
ax.set_xticklabels(xlabels)

ax.set_yticks([])
ax.grid(True)

plt.show()