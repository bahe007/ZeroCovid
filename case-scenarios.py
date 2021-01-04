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
    for ti in range(start, end):
        cases[ti] = N0*np.exp((R_eff-1)/d * (ti-start) )
    return cases

############## Rohdaten ##############
file_name = helpers.todays_filename()
helpers.download_todays_data_if_needed()

############## Ermittle die Fallzahlen über ganz Deutschland ##############
t0, cases = case_numbers.get_cases(file_name)
t = helpers.augment_t(t0, 90)

############## Konstanten ##############
d = 4.0 # Dauer der Infektiosität
scenario_start = "2020/12/24" # Startdatum, ab dem die Simulation einsetzt

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


# R=0.7
scenario_R_07 = simulate(start, end, 0.7, confirmed_incidence[start])
scenario_R_07_lower = simulate(start, end, 0.7-delta, confirmed_incidence[start])
scenario_R_07_upper = simulate(start, end, 0.7+delta, confirmed_incidence[start])

ax.plot(t[start:end], scenario_R_07[start:end], label="R_eff=0.7 (vgl. Israel)", color="b")
ax.fill_between(t[start:end], scenario_R_07_lower[start:end], scenario_R_07_upper[start:end], color='b', alpha=.5)

# R=0.8
scenario_R_08 = simulate(start, end+25, 0.8, confirmed_incidence[start])
scenario_R_08_lower = simulate(start, end+25, 0.8-delta, confirmed_incidence[start])
scenario_R_08_upper = simulate(start, end+25, 0.8+delta, confirmed_incidence[start])

ax.plot(t[start:end+25], scenario_R_08[start:end+25], label="R_eff=0.8 (vgl. Frühjahr)", color="g")
ax.fill_between(t[start:end+25], scenario_R_08_lower[start:end+25], scenario_R_08_upper[start:end+25], color='g', alpha=.5)


# R=0.9
scenario_R_09 = simulate(start, end+45, 0.9, confirmed_incidence[start])
scenario_R_09_lower = simulate(start, end+45, 0.9-delta, confirmed_incidence[start])
scenario_R_09_upper = simulate(start, end+45, 0.9+delta, confirmed_incidence[start])
ax.plot(t[start:end+45], scenario_R_09[start:end+45], label="R_eff=0.9", color="orange")
ax.fill_between(t[start:end+45], scenario_R_09_lower[start:end+45], scenario_R_09_upper[start:end+45], color='orange', alpha=.5)

# Tatsächliche Fallzahlen
ax.plot(t0[:-3], confirmed_incidence[:-3], label="Tatsächliche Fallzahlen (geglättet)", color="red")

# Achsen-Beschriftungen
xlabels = ["01. Juni", "01. Juli", "01. August", "01. September", "01. Oktober", "01. November", "01. Dezember", "01. Januar", "01. Februar", "01. März"]
ax.set_xticks(["2020/06/01", "2020/07/01", "2020/08/01", "2020/09/01", "2020/10/01", "2020/11/01", "2020/12/01", "2021/01/01", "2021/02/01", "2021/03/01"])
ax.set_xticklabels(xlabels)

ax.set_xlim(150, len(t))

ax.set_xlabel("Zeit")
ax.set_ylabel("7-Tages-Inzidenz")

ax.grid(True)


ax.legend(loc="upper left")
plt.show()