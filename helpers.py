import numpy as np
import csv
import datetime
import requests
import os

def moving_average(f, d=7):
    """Berechnet den gleitenden Durchschnitt der Länge `d` für einen Array. `d` ist dabei
    ungerade.

    Die `(d-1)/2` Einträge am Anfang und Ende werden mit den echten Werten aufgefüllt.
    """
    avg = np.zeros(len(f))
    delta = (d-1)//2

    for t in range(delta):
        avg[t] = f[t]

    for t in range(len(f)-delta, len(f)):
        avg[t] = f[t]

    for t in range(delta, len(f)-delta):
        avg[t] = sum(f[t-delta:t+delta+1])/d

    return avg

def classify_red_green(f):
    """Klassifiziert, ob der Landkreis eine grüne oder rote Zone ist.

    Da keine Landkreisgrenzen bekannt sind, werden keine gelben Zonen verwendet.

    Returns
    -------
    `1`, falls der Landkreis rot ist, sonst `0`
    """
    c = np.zeros(len(f))
    for t in range(len(f)):
        if f[t] > 0:
            c[t] = 1
        else:
            c[t] = 0
    return c

def classify_red_green_threshold(f, th):
    """Klassifiziert, ob der Landkreis eine grüne, gelbe oder rote Zone ist. 

    Eine grüne Zone ist er aber, wenn er mindestens `th` Tage keinen Fall hatte.
    Erst ab dann zählt er als grün, davor als gelb (quasi als Kandidat für eine
    grüne Zone).

    Returns
    -------
    - `2` falls der Landkreis rot ist
    - `1` falls der Landkreis gelb ist
    - `0` falls der Landkreis grün ist
    """

    case_free = 0 # #days with no cases
    c = np.zeros(len(f))
    for t in range(len(f)):
        if f[t] == 0:
            if case_free >= th:
                c[t] = 0
            else:
                c[t] = 1
            case_free += 1
        else:
            c[t] = 2
            case_free = 0
    return c

def green_zone_durations(f):
    """Ermittelt, wie lange (potentiell mehrere) Klassifikationen als grüne Zone andauerten

    Parameter
    ---------
    `f` ist die Ausgabe von `classify_red_green_threshold`. 

    Returns
    -------
    Eine Liste mit den Dauern der Green-Zone in Tagen. 
    """
    durations = []
    cur_duration = 0
    for t in range(len(f)):
        if f[t] != 0:
            if cur_duration > 0:
                durations.append(cur_duration)

            cur_duration = 0

        else:
            cur_duration += 1

    return durations


def generate_t(file_name):
    """Ermittelt das früheste und das älteste Datum, das im Datensatz vorkommt.
    Daraus wird dann die t-Achse erstellt.
    """
    start = "2050/00/00 00:00:00"
    end = ""

    with open(file_name, "r") as fp:
        csv_reader = csv.reader(fp, delimiter=',')

        title_row_read = False
        date_idx = 0
        for row in csv_reader:
            if title_row_read == False:
                title_row_read = True
                date_idx = row.index("Meldedatum")
                continue

            if row[date_idx] < start:
                start = row[date_idx]
            if row[date_idx] > end:
                end = row[date_idx]

    start = start[:-9]
    end = end[:-9]

    t = [start]
    date = datetime.datetime.strptime(start, "%Y/%m/%d")
    while t[-1] < end:
        t.append(date.strftime("%Y/%m/%d"))
        date += datetime.timedelta(days=1)

    return t

def augment_t(t, n_days):
    """Erweitert einen `t`-Array um `n_days` weitere Tage. 
    Das kann zum Beispiel verwendet werden, um verschiedene Szenarien vorzustellen.
    """
    t = t.copy()
    date = datetime.datetime.strptime(t[-1], "%Y/%m/%d") + datetime.timedelta(days=1)
    for _ in range(n_days):
        t.append(date.strftime("%Y/%m/%d"))
        date += datetime.timedelta(days=1)

    return t

def all_counties(file_name):
    """Ermittelt alle Landkreise im Datensatz
    """
    with open(file_name, "r") as fp:
        csv_reader = csv.reader(fp, delimiter=',')
        counties = set()

        title_row_read = False
        county_idx = 0
        for row in csv_reader:
            if title_row_read == False:
                title_row_read = True 
                county_idx = row.index("Landkreis")
                continue
            counties.add(row[county_idx])

        return counties

def todays_date():
    """Erstellt einen String mit dem heutigen Datum in menschenlesbaren Format.
    """
    date = datetime.datetime.now()
    return date.strftime("%d. %m. %Y")

def todays_filename():
    """Erstellt einen String mit dem Dateinamen, der für heute erwartet würde.
    """
    date = datetime.datetime.now()
    return 'data/{}.csv'.format(date.strftime("%d-%m-%Y"))

def download_data():
    """Lädt die aktuelle CSV-Datei vom RKI herunter und speichert sie in "data/RKI-dd-mm-yyyy.csv"
    """
    url = 'https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data'
    r = requests.get(url, allow_redirects=True)

    open(todays_filename(), 'wb').write(r.content)

def download_todays_data_if_needed():
    """Lädt die Datei mit den Daten von heute herunter, wenn sie nicht bereits existiert.
    """
    if not os.path.exists(todays_filename()):
        download_data()