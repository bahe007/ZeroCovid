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

ax.scatter(t[:], cases[:], color="grey", s=2, label="Tagesmeldungen")
ax.plot(t[:-3], helpers.moving_average(cases)[:-3], color="black", label="Gemittelte Werte")

# Achsenbeschritung
xlabels = ["Feb. 20", "Apr. 20", "Jun. 20", "Aug. 20", "Okt. 20", "Dez. 20", "Feb. 21", "Apr. 21", "Jun. 21", "Aug. 21"]
ax.set_xticks(["2020/02/01", "2020/04/01", "2020/06/01", "2020/08/01", "2020/10/01", "2020/12/01", "2021/02/01", "2021/04/01", "2021/06/01", "2021/08/01"])
ax.set_xticklabels(xlabels, fontsize=12)
ax.tick_params(axis='both', which='major', labelsize=12)
ax.tick_params(axis='both', which='minor', labelsize=12)
ax.grid(True)

ax.set_ylabel("Meldedaten des RKI (geglättet)", fontsize=12)

fig.set_figheight(9.6)
fig.set_figwidth(15)

plt.rcParams.update({'font.size': 12})
plt.subplots_adjust(left=0.075, bottom=0.05, right=0.95, top=0.95)
plt.title("Aktualisiert am {} um 08:00 UTC".format(helpers.todays_date()))
plt.legend(loc="upper left")
plt.savefig("images/daily-new-cases.png")