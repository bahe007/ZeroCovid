"""Löst das SIR-Modell mit konstanten Parametern numerisch mit scipy. Außerdem
wird gezeigt, dass das Exponentialmodell über einen langen Zeitraum das Ausbreitungs-
verhalten angemessen beschreibt, im Vergleich zum SIR-Modell.
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

############## Konstanten ##############
N = 30 # Anzahl betrachteter Tage
R_0 = 2.3 # Reproduktionszahl R0
d = 4.0 # mittlere Generationszeit
i0 = 10e-6 # Initialer Anteil der Infizierten
t = np.linspace(0, N-1, N) # Betrachteter Zeitraum, wobei an Tag 0 der Anteil an Infizierten gerade i0 ist

############## Numerische Lösung des SIR-Modells ##############
def sir(y, t):
    global R_0, d

    S, I, R = y

    ds = -R_0/d * I * S
    di = +R_0/d * I * S - I/d
    dr = + I/d

    return [ds, di, dr]

sol = odeint(sir, [1-i0, i0, 0.0], t)
s, i, r = sol[:, 0], sol[:, 1], sol[:, 2]

############## Anzahl der Neuinfizierten aus SIR-Modell ##############
# Die täglichen Neuinfektionen können nicht direkt aus den Infektionszahlen
# abgeleitet werden. Stattdessen ergibt sich die negative Änderung am 
# Susceptible-Anteil als Wert der Neuinfektionen.
neu = np.zeros(N-1)
for j in range(N-1):
    neu[j] = -(s[j+1]-s[j])

############## Anzahl der Neuinfizierten aus Exponentialmodell ##############
# Der Vorfaktor `alpha` dient zur Anpassung der Zahl der Neuinfektionen
# an die Werte, die aus dem SIR-Modell berechnet werden. Neuinfektionen 
# ergeben sich immer als Differenz aus heutigem und gestrigem Susceptible-Anteil.
# Dementsprechend liegen die ersten Neuinfektionen an Tag 1 vor. Also muss der
# Vorfaktor so angepasst werden, dass dieser erste Wert der Neuinfektionen
# exakt getroffen wird. 
alpha = neu[0]/np.exp((R_0-1)/d)
neu_infiziert_exp = alpha*np.exp(((R_0)-1)/d * (t[:]))

############## Ergebnisse anzeigen ##############
plt.plot(t[1:], neu, label="-ds(t) (SIR)")
plt.plot(t[1:], neu_infiziert_exp[1:], label="-ds(t) (exp)")

plt.yscale('log')
plt.legend(loc="upper left")
plt.grid()
plt.show()