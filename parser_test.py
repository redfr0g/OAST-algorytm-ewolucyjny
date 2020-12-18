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

# sumaryczne zapotrzebowanie dla wszystkich laczy
link_demands = {}

for link in linkList:
    link_demands[link.id] = 0
    for demand in demandList:
        for path in demand.paths:
            for id in path.linkIdList:
                if id == link.id:
                    link_demands[link.id] += int(demand.volume)

print(link_demands)
