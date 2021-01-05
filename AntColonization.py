import random, math, time
from PossionDisc import PossionDiscSampling as Sampling

# TODO: USE DICTIONARY TO HOLD DATA ON EDGES INSTEAD OF OBJECTS
# TODO: REDUCE THE NUMBER OF LOOPS PER ITERATION

W,H = 600,600

def dist(n1,n2):
    return math.sqrt((n1.pos[0]-n2.pos[0])**2 + (n1.pos[1]-n2.pos[1])**2)

def mapVal(s,a1,a2,b1,b2):
    return b1 + ((s - a1)*(b2-b1))/(a2-a1);

def determineEdgeValue(dist,div=1):
    return (1000/(dist/div))

def intJoin(x, y):
    return x*100+y

# def intJoin(x,y):
#     a = int(''.join([str(x),str(y)]))
#     return a

def generatePoints(num,margin,seed=0):
    random.seed(seed)
    points = []
    for i in range(num):
        points.append((random.randint(margin,W-margin),random.randint(margin,H-margin)))
    random.seed(time.time())
    return points

class Node():
    def __init__(self,i,pos):
        self.edges = []
        self.tag = i
        self.pos = pos

    def preferredPath(self,ant):
        visitedNum = 0
        visitedTotalWeight = 0
        sample = []
        sampleSize = 0
        for edge in self.edges:                # FOR LOOP RAN EVERY STEP IN THE TOUR, ITERATIONS = EDGES
            if edge.otherNode(self).tag not in ant.visited:
                if edge.weight > 0:
                    visitedNum += 1
                    visitedTotalWeight += edge.weight
                sample.append(edge)
                sampleSize += 1
        return self.finalEdge(sample,sampleSize,visitedTotalWeight,visitedNum)

    def finalEdge(self,sample,sampleSize,totalWeight,visitNum):
        rand = random.random()
        upper = 0
        for edge in sample:
            base = upper
            if edge.weight > 0:
                prob = (edge.weight / totalWeight)  * (visitNum / sampleSize)
            else:
                prob = (1 / sampleSize)
            upper = base+prob
            if base < rand < upper:
                return edge

class Edge():
    def __init__(self,i,total,node1,node2):
        self.tag = i
        self.nodes = [node1,node2]
        self.length = dist(self.nodes[0],self.nodes[1])
        self.value = determineEdgeValue(self.length,1.5)
        self.weight = 0.0

        for node in self.nodes:
            node.edges.append(self)

    def otherNode(self,node):
        return self.nodes[(self.nodes.index(node)+1)%2]

    def travelOn(self,currentNode):
        self.weight += self.value
        return self.otherNode(currentNode)

# Algorithm controller
class AntColony():
    def __init__(self,populationSize):
        self.ant = Ant(self)
        self.popSize = populationSize
        self.reset()

    def reset(self):
        self.nodes = []
        self.edges = []
        self.edgeDict = {}
        self.solution = None
        self.edgesCreated = False
        self.nodeCounter = 0
        self.startTime = time.time()

    # add nodes to list when needed
    def addNode(self,*points):
        for pos in points:
            self.nodes.append(Node(self.nodeCounter,pos))
            self.nodeCounter += 1

    def findEdgeBetweenNodes(self,tag1,tag2):
        return self.edgeDict[intJoin(*sorted([tag1,tag2]))]

    # create all edges connecting the nodes
    def generateEdges(self):
        self.edgesCreated = True
        count = 0
        for first in range(0,self.nodeCounter-1):
            for second in range(first+1,self.nodeCounter):
                edge = Edge(count,self.nodeCounter,self.nodes[first],self.nodes[second])
                self.edges.append(edge)
                self.edgeDict[intJoin(first,second)] = edge
                count += 1

    def runPopulation(self):
        self.startTime = time.time()
        if self.edgesCreated == False:
            self.generateEdges()
            self.edgesCreated = True
        for i in range(self.popSize):
            self.ant.tour()

    def log(self,show=False):
        worst = self.ant.longestTrip
        best = self.ant.shortestTrip[0]
        if show:
            print("Data Points: %i"%self.nodeCounter)
            print("Number Of Ants: %i"%self.popSize)
            print("Shortest Path Found: %.2f units"%best)
            print("Path Improvement: %.2f%s"%((worst-best)/worst*100,"%"))
            print("Completed In: %.4f seconds"%(time.time()-self.startTime))

        return {
            'points'    : self.nodeCounter,
            'ants'      : self.popSize,
            'solution'  : best,
            'worst'     : worst,
            'time'      : (time.time()-self.startTime)
        }

class Ant():
    def __init__(self,parent):
        self.parent = parent
        self.reset()

    def reset(self):
        self.location = None;
        self.start = None
        self.visited = []
        self.usedEdges = []
        self.longestTrip = None
        self.shortestTrip = None
        self.distance = 0

    def updateStats(self):
        if self.longestTrip == None or self.longestTrip < self.distance:
            self.longestTrip = self.distance
        elif self.shortestTrip == None or self.shortestTrip[0] > self.distance:
            self.shortestTrip = [self.distance,self.visited]
            self.parent.solution = self.shortestTrip

    def tour(self):
        self.location = random.choice(self.parent.nodes)
        self.start = self.location
        self.distance = 0
        self.visited = []
        self.usedEdges = []
        self.visited.append(self.location.tag)

        for i in range(self.parent.nodeCounter-1):
            self.takePath(self.location.preferredPath(self))

        self.takePath(self.parent.findEdgeBetweenNodes(self.location.tag,self.start.tag))
        pathWeight = determineEdgeValue(self.distance,self.parent.nodeCounter)
        for edge in self.usedEdges:
            edge.weight += pathWeight

        self.updateStats()

    def takePath(self,path):
        self.usedEdges.append(path)
        self.distance += path.length
        self.location = path.travelOn(self.location)
        self.visited.append(self.location.tag)


if __name__ in '__main__':
    s = time.time()
    c = AntColony(10000)
    c.addNode(*generatePoints(15,25,0))
    c.generateEdges()
    c.runPopulation()
    c.log(True)
