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
matrix = np.array([helpers.moving_average(cases_per_county[county])[:-3]+1 for county in zeroDaysPerCounty.keys()])

############## Darstellung ##############

fig, ax = plt.subplots()
ax.set_ylabel("Landkreise bzw. kreisfreie Städte", fontsize=12)

xtick_positions = [t.index("2020/02/01"), t.index("2020/03/01"), t.index("2020/04/01"), t.index("2020/05/01"), t.index("2020/06/01"), t.index("2020/07/01"), t.index("2020/08/01"), t.index("2020/09/01"), t.index("2020/10/01"), t.index("2020/11/01"), t.index("2020/12/01"), t.index("2021/01/01"), t.index("2021/02/01"), t.index("2021/03/01")]
xlabels = ["1. Februar", "", "1. April", "", "1. Juni", "", "1. August", "", "1. Oktober", "", "1. Dezember", "", "1. Februar", ""]

cax = ax.matshow(matrix, cmap=matplotlib.cm.Reds, norm=matplotlib.colors.LogNorm())

ax.set_xticks(xtick_positions)
ax.set_xticklabels(xlabels, fontsize=12)

ax.set_yticks([])
ax.grid(False)

ax.tick_params(axis='both', which='major', labelsize=12)
ax.tick_params(axis='both', which='minor', labelsize=12)

fig.set_figheight(9.6)
fig.set_figwidth(15)

cbar = fig.colorbar(cax, ticks=[1, 11, 51, 101, 501])
cbar.ax.set_yticklabels(["0 Neuininfizierte pro Tag", "10 Neuinfizierte pro Tag", "50 Neuinfizierte pro Tag", "100 Neuinfizierte pro Tag", "500 Neuinfizierte pro Tag"], fontsize=12) 

plt.rcParams.update({'font.size': 12})
plt.subplots_adjust(left=0.0, bottom=0.1, right=0.9, top=0.9)
plt.title("Aktualisiert am {} um 08:00 UTC".format(helpers.todays_date()), y=1.05)
plt.savefig("images/counties-2d-view.png")