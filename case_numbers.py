"""Helpers for obtaining the case raw numbers.
"""
import numpy as np
import csv
import helpers

def get_cases(file_name, states=None):
    """Ermittelt die täglichen Neuinfektionen aus RKI-Daten. 

    Gibt den Zeitraum und die täglichen Neuinfektionen zurück. Optional
    kann eine Begrenzung auf eine Liste von Bundesländern angegeben werden
    """
    t = helpers.generate_t(file_name)
    cases = np.zeros(len(t))

    caseNumberIdx = 0
    dateIdx = 0
    stateIdx = 0

    with open(file_name, "r") as fp: 
        csv_reader = csv.reader(fp, delimiter=',')

        title_row_read = False
        for row in csv_reader:
            if not title_row_read:
                caseNumberIdx = row.index("AnzahlFall")
                dateIdx = row.index("Meldedatum")
                stateIdx = row.index("Bundesland")
                title_row_read = True
                continue

            if states == None or ( row[stateIdx] in states ):
                caseNumber = row[caseNumberIdx]
                date = row[dateIdx][:-9]

                cases[t.index(date)] = cases[t.index(date)] + float(caseNumber)

    return t, cases

def get_cases_per_county(file_name):
    """Ermittelt die täglichen Neuinfektionen pro Landkreis aus RKI-Daten.
    """
    counties = helpers.all_counties(file_name)
    t = helpers.generate_t(file_name)

    cases_per_county = dict()
    for county in counties:
        cases_per_county[county] = np.zeros(len(t))

    caseNumberIdx = 0
    dateIdx = 0
    countyIdx = 0

    with open(file_name, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        title_row_read = False
        for row in csv_reader:
            if not title_row_read:
                caseNumberIdx = row.index("AnzahlFall")
                dateIdx = row.index("Meldedatum")
                countyIdx = row.index("Landkreis")
                title_row_read = True
                continue

            county = row[countyIdx]
            caseNumber = row[caseNumberIdx]
            date = row[dateIdx][:-9]

            cases_per_county[county][t.index(date)] += int(caseNumber)
    
    return t, counties, cases_per_county