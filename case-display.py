import helpers
import case_numbers

import matplotlib.pyplot as plt

############## Rohdaten ##############
file_name = helpers.todays_filename()
helpers.download_todays_data_if_needed()

############## Konstanten ##############
t, cases = case_numbers.get_cases(file_name)

############## Zeichne Fallzahlen ##############
fig, ax = plt.subplots()

ax.plot(t[:-3], helpers.moving_average(cases)[:-3])

# Achsenbeschritung
xlabels = ["1. Februar", "1. April", "1. Juni", "1. August", "1. Oktober", "1. Dezember", "1. Februar"]
ax.set_xticks(["2020/02/01", "2020/04/01", "2020/06/01", "2020/08/01", "2020/10/01", "2020/12/01", "2021/02/01"])
ax.set_xticklabels(xlabels)
ax.grid(True)

ax.set_ylabel("Meldedaten des RKI (geglättet)")

fig.set_figheight(9.6)
fig.set_figwidth(15)
plt.savefig("images/daily-new-cases.png")