import json, math
import AntColonization

def dist(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

class RouteController():
    def __init__(self,iterations,NumOfOutposts=1):
        self.mapData = json.loads(open('MapData.json','r').read())
        self.islandDict = {}
        self.ACO = AntColonization.AntColony(iterations)
        self.solution = None
        self.center = [0,0]
        self.outpostNum = NumOfOutposts

    def reset(self):
        self.ACO.reset()
        self.ACO.ant.reset()

    def addIsland(self,*islandNames):
        for name in islandNames:
            try:
                pos = self.mapData['islands'][name]
                self.islandDict[self.ACO.nodeCounter] = name
                self.center = [sum([x,y]) for x,y in zip(self.center,pos)]
                self.ACO.addNode(pos)
            except KeyError:
                print("%s Not Found."%name)

    def orderOutposts(self):
        self.center = [pos/self.ACO.nodeCounter for pos in self.center]
        currentIslands = list(self.islandDict.values())
        ranking = []
        for name,location in self.mapData['outposts'].items():
            if name not in currentIslands:
                ranking.append([name,dist(self.center,location)])

        return (name for name, dist in sorted(ranking, key= lambda x : x[1])[:self.outpostNum])

    def calculateRoute(self):
        final = []
        for outpost in self.orderOutposts():
            self.addIsland(outpost)
        if self.ACO.nodeCounter > 3:
            self.ACO.generateEdges()
            self.ACO.runPopulation()

            self.solution = self.ACO.ant.shortestTrip

            return self.solution
        else:
            print("Not Enough Islands Given")
            return

if __name__ in "__main__":
    plotter = RouteController(5000)

    plotter.addIsland(
        "Galleon's Grave Outpost",
        "Kraken's Fall",
        "Shark Tooth Key",
        "Isle of Last Words",
        "Shiver Retreat",
        "Tri-Rock Isle",
        "Shipwreck Bay",
        "Dagger Tooth Outpost",
        "The Sunken Grove"
    )

    plotter.generateRoute()
