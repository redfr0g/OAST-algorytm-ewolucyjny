import network_parser
from pyvis.network import Network

# Parse network file
linkList, demandList = network_parser.parseXML('net12_1.xml')

net = Network()
nodes = []

# Get all nodes
for link in linkList:
    if link.startNode not in nodes:
        nodes.append(link.startNode)
    if link.endNode not in nodes:
        nodes.append(link.endNode)

# Get unqiue nodes
nodes = list(set(nodes))

# Add nodes
for node in nodes:
    net.add_node(node)

# Add edges
for link in linkList:
    net.add_edge(link.startNode, link.endNode)

# Print graph
net.show("network.html")

