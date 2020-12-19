'''
OAST - plik testowy parsera plików

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

# Print all links
# for link in linkList:
#    print(link.startNode, link.endNode, link.numberOfModules, link.moduleCost, link.linkModule)
#
# # Print all demands
# for demand in demandList:
#    print(demand.startNode, demand.endNode, demand.volume)
#    print(len(demand.paths))
#    for path in demand.paths:
#        print(path.id, path.linkIdList)

flow_matrix = {}
demands = []

for demand in demandList:
    volume = demand.volume
    while sum(demands) != demand.volume:
        demands = []
        for path in demand.paths:
            allocation = random.randint(0, volume - sum(demands))
            flow_matrix[demand.id, path.id] = allocation
            demands.append(allocation)

print("Macierz zapotrzebowan: ")
for demand in demandList:
    row = []
    for path in demand.paths:
        row.append(flow_matrix[demand.id, path.id])
    print(row)