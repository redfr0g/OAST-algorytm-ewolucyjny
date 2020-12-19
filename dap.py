'''
OAST - algorytm genetyczny dla problemu DAP

# linkList
startNode - wezel poczatkowy
endNode - wezel koncowy
numberOfModules - ilosc wlokien optycznych w kablu
moduleCost - koszt wlokna
linkModule - ilosc lambda w wloknie

# demandList
startNode - wezel poczatkowy
endNode - wezel koncowy
volume - ilosc zapotrzebowania
paths - sciezki do zapotrzebowaniu
linkId - identyfikator łącza w zapotrzebowaniu

'''

import network_parser
import random

# Parse network file
linkList, demandList = network_parser.parseXML('net4.xml')

# Alokacja pustej macierzy wymagan
flowMatrix = {}
demands = []

# Generacja macierzy wymagan
for demand in demandList:
    volume = demand.volume
    # Wyzeruj liste dla nowego wymagania
    demands = []
    # Jezeli rozdzielone losowo wymagania nie sumuja sie do calkowitego wymagania to powtorz alokacje wymagan
    while sum(demands) != demand.volume:
        # Wyzeruj liste dla ponownej alokacji
        demands = []
        for path in demand.paths:
            # Przydziel losowe wymagania od 0 do calkowitego wymagania jakie zostalo do rozdzielenia
            allocation = random.randint(0, volume - sum(demands))
            # Przypisz wymaganie
            flowMatrix[demand.id, path.id] = allocation
            demands.append(allocation)

# Wypisz macierz zapotrzebowan
print("Macierz zapotrzebowan: ")
for demand in demandList:
    row = []
    for path in demand.paths:
        row.append(flowMatrix[demand.id, path.id])
    print(row)

# Tworzenie pustego slownika obciazen dla laczy
linkLoad = {}
for link in linkList:
    linkLoad[link.id] = 0

# Obliczenie obciazenia laczy
for demand in demandList:
    for path in demand.paths:
        for linkId in path.linkIdList:
            linkLoad[linkId] += flowMatrix[demand.id, path.id]

print("Lista obciazen dla kazdego lacza: {}".format(linkLoad))
print("Calkowite obciazenie sieci: {}".format(sum(linkLoad.values())))

# Obliczenie funkcji maksymalnego obciazenia
for link in linkList:
    if link.id == 1:
        # Dla pierwszego lacza przypisz wartosc bez porownywania
        loadMaximum = linkLoad[link.id] - link.numberOfModules
    else:
        # Dla kolejnych lacz wybierz wartosc maksymalna
        loadMaximum = max(linkLoad[link.id] - link.numberOfModules, loadMaximum)

print("Maksymalna wartosc obciazenia lacza: {}".format(loadMaximum))
