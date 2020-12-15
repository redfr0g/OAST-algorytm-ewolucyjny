import network_parser

# Parse network file
linkList, demandList = network_parser.parseXML('net4.xml')

# Print all links
for link in linkList:
   print(link.id, link.startNode, link.endNode, link.numberOfModules, link.moduleCost, link.linkModule)

# Print all demands
for demand in demandList:
   print(demand.id, demand.startNode, demand.endNode, demand.volume)
   for path in demand.paths:
       print(path.id, path.linkIdList)
