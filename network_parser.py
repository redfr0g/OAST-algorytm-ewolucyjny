'''

OAST - Network input file parser module

'''
import xml.etree.ElementTree as ET

# Link class
class Link:
    def __init__(self, id, startNode, endNode, numberOfModules, moduleCost, linkModule):
        self.id = id
        self.startNode = startNode
        self.endNode = endNode
        self.numberOfModules = numberOfModules
        self.moduleCost = moduleCost
        self.linkModule = linkModule

# Demand class
class Demand:
    def __init__(self, id, startNode, endNode, volume, paths):
        self.id = id
        self.startNode = startNode
        self.endNode = endNode
        self.volume = volume
        self.paths = paths

# Path class
class Path:
    def __init__(self, id, linkIdList):
        self.id = id
        self.linkIdList = linkIdList


# parsing function
def parseXML(file):
    # get xml root
    tree = ET.parse(file)
    root = tree.getroot()

    linkList = []
    demandList = []

    # get all links and attributes
    for link in root.findall('./links/link'):
        id = link.attrib['id']
        startNode = link.find('startNode').text
        endNode = link.find('endNode').text
        numberOfModules = link.find('numberOfModules').text
        moduleCost = link.find('moduleCost').text
        linkModule = link.find('linkModule').text

        newLink = Link(id, startNode, endNode, numberOfModules, moduleCost, linkModule)
        linkList.append(newLink)

    # get all demands and attributes
    for demand in root.findall('./demands/demand'):

        pathList = []

        id = demand.attrib['id']
        startNode = demand.find('startNode').text
        endNode = demand.find('endNode').text
        volume = demand.find('volume').text

        # get all paths for each demand
        for path in demand.findall('./paths/path'):

            pathId = path.attrib['id']
            linkIdList = []
            for linkId in path.findall('linkId'):
                linkIdList.append(linkId.text)

            newPath = Path(pathId, linkIdList)
            pathList.append(newPath)

        paths = pathList
        newDemand = Demand(id, startNode, endNode, volume, paths)
        demandList.append(newDemand)

    return linkList, demandList
