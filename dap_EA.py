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
from copy import deepcopy

import network_parser
import random
from operator import itemgetter

# Parse network file
linkList, demandList = network_parser.parseXML('net12_1.xml')


class Chromosome:

    def __init__(self, linkList, demandList):
        self.flowMatrix = {}
        self.geneList = []
        self.linkLoad = {}
        self.loadMaximum = 0

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
                    self.flowMatrix[demand.id, path.id] = allocation
                    demands.append(allocation)

        #tworzenie pomocniczej listy genów
        for demand in demandList:
            gene = []
            for path in demand.paths:
                gene.append(self.flowMatrix[demand.id, path.id])
            self.geneList.append(gene)

        self.setLinkLoad()
        self.sefLoadMax()


    def setLinkLoad (self):
        # Tworzenie pustego slownika obciazen dla laczy
        for link in linkList:
            self.linkLoad[link.id] = 0

        # Obliczenie obciazenia laczy
        for demand in demandList:
            for path in demand.paths:
                for linkId in path.linkIdList:
                    self.linkLoad[linkId] += self.flowMatrix[demand.id, path.id]
        #print("Lista obciazen dla kazdego lacza: {}".format(self.linkLoad))
        #print("Calkowite obciazenie sieci: {}".format(sum(self.linkLoad.values())))

    def sefLoadMax(self):
        # Obliczenie funkcji maksymalnego obciazenia
        for link in linkList:
            if link.id == 1:
                # Dla pierwszego lacza przypisz wartosc bez porownywania
                self.loadMaximum = self.linkLoad[link.id] - link.numberOfModules*link.linkModule
            else:
                # Dla kolejnych lacz wybierz wartosc maksymalna
                self.loadMaximum = max(self.linkLoad[link.id] - link.numberOfModules*link.linkModule, self.loadMaximum)


""" Algorytm Ewolucyjny

1. Evaluate the fitness of each individual in the population (time limit, sufficient fitness achieved, etc.)
2. Select the fittest individuals for reproduction. (Parents)
3. Breed new individuals through crossover and mutation operations to give birth to offspring.
4. Replace the least-fit individuals of the population with new individuals.

"""

current_population = []
population_size = 6
#lista wszystkich populacji (generacji)
populationList = []

#najlepsze chormosomy z populacji, które zostają rodzicami
parents = []
number_of_parents = 2

#Crossover + Mutacja
pstwo_crossover = 0.5
pstwo_mutation = 0.5

i = 0
#1.Generujemy pierwszą populację
while i < population_size:
    newChromosome = Chromosome(linkList, demandList)
    current_population.append(newChromosome)
    i += 1

populationList.append(deepcopy(current_population))

#2.Wybieramy najlepsze chormosomy z populacji - czyli takie, które mają namniejszą wartość loadMaximum

#najpierw sortujemy chormosomy w populacji po loadMaximum w pierwszej generacji
def funcSortChormosomes(e):
  return e.loadMaximum

current_population.sort(key=funcSortChormosomes)

'''
print("\nBieżąca populacja (chromosomy):")
i = 0
while i < population_size:
    print(current_population[i], " ", current_population[i].loadMaximum)
    i += 1
print()
'''
#Kryterium stopu
max_iteration = 150
max_generation = 150
max_mutation = 800
max_imprv_count = 30

number_of_mutation = 0
imprv = False
impr_count = 0

it = 0
while it < max_iteration and len(populationList) < max_generation and number_of_mutation < max_mutation and impr_count < max_imprv_count:
#Wybieramy rodziców - 4 pierwsze chromosomy w posortowanej populacji
    parents.clear()
    for i in range(0, number_of_parents):
        newParent = deepcopy(current_population[i])
        parents.append(newParent)

    i = 0
    '''
    print("\nParents (4 najlepsze chormosomy):")
    while i < number_of_parents:
        print(parents[i]," ", parents[i].loadMaximum)
        i += 1
    '''

    #if random.uniform(0, 1)) < pstwo_crossover:

    #print(len(demandList)/2)
    offSpringList = []

    i = 0
    j = 0
    #Generowanie potomstwa:
    # Crossover - połowa genów jedengo rodzica i połowa genów drugiego rodzica
    # Mutacja - zmieniamy obciążenie dwóch losowych ścieżek w losowym żądaniu

    while i < number_of_parents:
        newFlowMatrix = {}

        for demand in demandList:
            if random.uniform(0, 1) > pstwo_crossover:
                for path in demand.paths:
                    newFlowMatrix[demand.id, path.id] = parents[i].flowMatrix[demand.id, path.id]
            else:
                for path in demand.paths:
                    newFlowMatrix[demand.id, path.id] = parents[i + 1].flowMatrix[demand.id, path.id]

        i += 2
        j += 1

        offSpring = Chromosome(linkList, demandList)
        offSpring.flowMatrix = newFlowMatrix

        """
        print("\nRodzic {}".format(i-2))
        print(parents[i-2].flowMatrix)
        print("\nRodzic {}".format(i-1))
        print(parents[i-1].flowMatrix)
        print("\nPotomstwo {}".format(j))
        print(offSpring.flowMatrix)
        """

        #Mutacja - zmieniamy obciążenie dwóch losowych ścieżek w losowym żądaniu
        if random.uniform(0, 1) > pstwo_mutation:
            number_of_mutation += 1
            # losowe żądanie
            randomDemandId = random.randint(0, len(demandList)-1) + 1
            # losowe ścieżki
            pathLen = len(demandList[randomDemandId-1].paths)
            pathRandomOne = random.randint(1, pathLen)
            pathRandomTwo = pathRandomOne

            # jeżeli dane zapotrzebowanie ma tylko jedną ścieżkę to nie da się przeprowadzić mutacji
            if pathLen == 1:
                break
            while pathRandomTwo == pathRandomOne:
                pathRandomTwo = random.randint(1, pathLen)

            pathLoadValueOne = offSpring.flowMatrix[randomDemandId, pathRandomOne]
            pathLoadValueTwo = offSpring.flowMatrix[randomDemandId, pathRandomTwo]

            #zamiana
            offSpring.flowMatrix[randomDemandId, pathRandomOne] = pathLoadValueTwo
            offSpring.flowMatrix[randomDemandId, pathRandomTwo] = pathLoadValueOne

            #print("Potomstwo {} po mutacji genu {}, zamiana ścieżek {} i {}".format(j, randomDemandId,pathRandomOne, pathRandomTwo))
            #print(offSpring.flowMatrix)
        offSpringList.append(offSpring)

    '''
    print("\nOld LoadMax")
    for i in range(0, j):
        print(current_population[i].loadMaximum)
    '''

    #Ewaluacja
    for offSpring in offSpringList:
        offSpring.setLinkLoad()
        offSpring.sefLoadMax()

    '''
    print("New LoadMax")
    for offSpring in offSpringList:
        print(offSpring.loadMaximum)
    '''

    #4. Tworzenie nowej populacji - wybieramy najlepszych osobników

    # tworzymy wspólną listę wszytskich chormosomów starych i nowych
    newChromosomeList = current_population + offSpringList

    """
    print("Nieposortowana połaczona lista chormosomów starych i potomków")
    for chromosome in newChromosomeList:
        print(chromosome.loadMaximum)
    """

    # Sotrujemy listę wszytskich chromosomów
    newChromosomeList.sort(key=funcSortChormosomes)

    """
    print("Posortowana połaczona lista chormosomów starych i potomków")
    for chromosome in newChromosomeList:
        print(chromosome.loadMaximum)
    """

    # Tworzymy nową generację wybierając najlepszych
    current_population.clear()
    current_population = newChromosomeList[0:population_size]
    populationList.append(deepcopy(current_population))

    '''
    print("New Population {}".format(len(populationList)))
    for chromosome in current_population:
        print(chromosome.loadMaximum)
    '''
    it += 1


    if populationList[-1][0].loadMaximum < populationList[-2][0].loadMaximum:
        imprv = True
        impr_count = 0
    else:
        imprv = False
        impr_count += 1


print()
print("Liczba iteracji: {}".format(it))
print("Liczba populacji: {}".format(len(populationList)))
print("Liczba mutacji: {}".format(number_of_mutation))
print("Liczba populacji bez poprawy: {}".format(impr_count))
stop_reason = ""
if it >= max_iteration:
    stop_reason = "Przekroczono dopuszczalną liczbę iteracji"
elif len(populationList) >= max_generation:
    stop_reason = "Przekroczono dopuszczalną liczbę genracji"
elif number_of_mutation >= max_mutation:
    stop_reason = "Przekroczono dopuszczalną liczbę mutacji"
elif impr_count >= max_imprv_count:
    stop_reason = "Przekroczono dopuszczalną liczbę genracji bez poprawy"

print("Kryterium stopu: {}".format(stop_reason))
print("Najlepsze rozwiązanie minF = {}".format(populationList[-1][0].loadMaximum))
