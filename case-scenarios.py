"""Zeigt verschiedene Szenarien auf, wie sich die Fallzahlen entwicklen könnten. 

Dazu wird ein einfaches exponentielles Modell verwendet. Offensichtlich ist dieses
Modell nicht geeignet, konkrete Prognosen zu treffen. Um das zu verdeutlichen, werden
Unsicherheitsintervalle angegeben. 

Diese ergeben sich jeweils für den Fall, dass die effektive Reproduktionszahl 0,025 
größer oder kleiner als die zentrale Tendenz ist. Für das Szenario R_eff=0,7
werden beispielsweise die Grenzen bei R_eff=0,675 und R_eff=0,725 gezogen. 
"""
import helpers
import case_numbers
import datetime

import numpy as np
import matplotlib.pyplot as plt

############## Szenarien ##############
def simulate(start, end, R_eff, N0):
    """Stellt ein Szenario mit konstanter Reproduktionszahl bereit.

    Parameter
    ---------
    - `start`: Index im `t`-Array, ab dem simuliert werden soll
    - `end`: Index für den `t`-Array, bis zu dem simuliert werden soll
    - `R_eff`: effektive Kontaktrate (bzw `mu` für `R_eff < 0`)
    - `N0`: Startwert der Infektionszahlen
    """
    global t
    cases = np.zeros(len(t))
    d = 4.0
    for ti in range(start, min(end, len(t))):
        cases[ti] = N0*np.exp(np.log(R_eff)/d * (ti-start) )
    return cases

############## Rohdaten ##############
file_name = helpers.todays_filename()
helpers.download_todays_data_if_needed()

############## Ermittle die Fallzahlen über ganz Deutschland ##############
t0, cases = case_numbers.get_cases(file_name)
t = helpers.augment_t(t0, 90)

############## Konstanten ##############
d = 4.0 # Dauer der Infektiosität

now = datetime.datetime.now()
start_date = now-datetime.timedelta(days=4) # Startdatum der Szenarien ist standardmäßig vor vier Tagen
scenario_start = start_date.strftime("%Y/%m/%d")

############## Zeichne Fallzahlen ##############
fig, ax = plt.subplots()

confirmed_incidence = helpers.moving_average(cases)*7/810

start = t.index(scenario_start)
end = start+50

# absoluter Unsicherheitsfaktor in R
delta = 0.025

# Zielgrößen
ax.plot(t,[10]*len(t), c="gray", label="7-Tagesinzidenz 10")

# Szenarien zeichnen
R = [0.7, 0.8, 0.9]
colors = ["green", "orange", "red"]
for i in range(len(R)):
    end = start + int(np.log(10/confirmed_incidence[start])*d/np.log(R[i]+delta))

    lower_bound = simulate(start, end, R[i]-delta, confirmed_incidence[start])
    upper_bound = simulate(start, end, R[i]+delta, confirmed_incidence[start])

    ax.fill_between(t[start:end], lower_bound[start:end], upper_bound[start:end], color=colors[i], alpha=.5, label="R_eff={:.1f}".format(R[i]))

# Tatsächliche Meldedaten
ax.plot(t0[:-3], confirmed_incidence[:-3], label="Meldedaten des RKI (geglättet)", color="black")
ax.scatter(t0[:], cases[:]*7/810, color="grey", s=2, label="Tagesmeldungen")

# Achsen-Beschriftungen
xlabels = ["Sept. 20", "Okt. 20", "Nov. 20", "Dez. 20", "Jan. 21", "Feb. 21", "Mrz. 21", "Apr. 21", "Mai 21", "Jun. 21", "Jul. 21", "Aug. 21", "Sept. 21", "Oct. 21", "Nov. 21"] # "Jun. 20", "Jul. 20", "Aug. 20", 
ax.set_xticks(["2020/09/01", "2020/10/01", "2020/11/01", "2020/12/01", "2021/01/01", "2021/02/01", "2021/03/01", "2021/04/01", "2021/05/01", "2021/06/01", "2021/07/01", "2021/08/01", "2021/09/01", "2021/10/01", "2021/11/01"]) # "2020/06/01", "2020/07/01", "2020/08/01", 
ax.set_xticklabels(xlabels, fontsize=12)
ax.set_xlim(210, len(t)-1)

ax.set_ylabel("7-Tages-Inzidenz", fontsize=12)
ax.tick_params(axis='both', which='major', labelsize=12)
ax.tick_params(axis='both', which='minor', labelsize=12)

ax.grid(True)


ax.legend(loc="upper left")
fig.set_figheight(9.6)
fig.set_figwidth(15)

plt.rcParams.update({'font.size': 12})
plt.subplots_adjust(left=0.075, bottom=0.05, right=0.95, top=0.95)
plt.title("Aktualisiert am {} um 08:00 UTC".format(helpers.todays_date()))
plt.savefig("images/scenario.png")