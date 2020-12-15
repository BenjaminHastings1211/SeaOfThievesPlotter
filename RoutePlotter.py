import json
import AntColonization

tour = AntColonization.AntColony(100)

data = json.loads(open('MapData.json','r').read())['islands']
islandDict = {}

def addIsland(name):
    pos = data[name]
    islandDict[tour.nodeCounter] = name
    tour.addNode(pos)
    try:
        pass

    except KeyError:
        print("Island Not Found.")

def generateRoute():
    tour.generateEdges()
    tour.runPopulation()
    dist, path = tour.finalTour(tour.nodes[0])
    print(dist)
    for island in path:
        print(islandDict[island])

# addIsland('Sanctuary Outpost')
# addIsland("Sailor's Bounty")
# addIsland("Lone Cove")
# addIsland("Hidden Spring Keep")
# addIsland("Crescent Isle")
# addIsland("The North Star Seapost")
# addIsland("Picaroon Palms")
# addIsland("Sea Dog's Rest")
# addIsland("Old Faithful Isle")
# addIsland("Keel Haul Fort")

addIsland("Galleon's Grave Outpost")
addIsland("Kraken's Fall")
addIsland("Shark Tooth Key")
addIsland("Isle of Last Words")
addIsland("Shiver Retreat")
addIsland("Tri-Rock Isle")
addIsland("Shipwreck Bay")
addIsland("Dagger Tooth Outpost")
addIsland("The Sunken Grove")
addIsland("Skull Keep")
addIsland("The Crooked Masts")
addIsland("Three Paces East Seapost")
addIsland("Liar's Backbone")
addIsland("Wanderers Refuge")
addIsland("Cannon Cove")
addIsland("Hidden Spring Keep")



generateRoute()
