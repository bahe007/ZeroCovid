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
ax.plot(t,[7]*len(t), c="black", label="containcovid-pan.eu - Ziel")
ax.plot(t, [50]*len(t), c="grey", label="Ziel der Bundesregierung")

# Szenarien zeichnen
R = [0.7, 0.8, 0.9]
colors = ["green", "blue", "purple"]
for i in range(len(R)):
    end = start + int(np.log(7/confirmed_incidence[start])*d/np.log(R[i]+delta))

    lower_bound = simulate(start, end, R[i]-delta, confirmed_incidence[start])
    upper_bound = simulate(start, end, R[i]+delta, confirmed_incidence[start])

    ax.fill_between(t[start:end], lower_bound[start:end], upper_bound[start:end], color=colors[i], alpha=.5, label="R_eff={:.1f}".format(R[i]))

# Tatsächliche Meldedaten
ax.plot(t0[:-3], confirmed_incidence[:-3], label="Meldedaten des RKI (geglättet)", color="red")

# Achsen-Beschriftungen
xlabels = ["01. Juni", "01. Juli", "01. August", "01. September", "01. Oktober", "01. November", "01. Dezember", "01. Januar", "01. Februar", "01. März", "01. April"]
ax.set_xticks(["2020/06/01", "2020/07/01", "2020/08/01", "2020/09/01", "2020/10/01", "2020/11/01", "2020/12/01", "2021/01/01", "2021/02/01", "2021/03/01", "2021/04/01"])
ax.set_xticklabels(xlabels)

ax.set_xlim(180, len(t)-1)

ax.set_xlabel("Zeit")
ax.set_ylabel("7-Tages-Inzidenz")

ax.grid(True)


ax.legend(loc="upper left")
fig.set_figheight(9.6)
fig.set_figwidth(15)
plt.savefig("images/scenario.png")