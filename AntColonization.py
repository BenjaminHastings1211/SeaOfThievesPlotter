import random, math, time
from PossionDisc import PossionDiscSampling as Sampling

W,H = 600,600

def dist(n1,n2):
    return math.sqrt((n1.pos[0]-n2.pos[0])**2 + (n1.pos[1]-n2.pos[1])**2)

def mapVal(s,a1,a2,b1,b2):
    return b1 + ((s - a1)*(b2-b1))/(a2-a1);

def determineEdgeValue(dist,div=1):
    return (1000/(dist/div))

def intJoin(x, y):
    return x*100+y

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
        probList = self.generateProbability(ant)
        rand = random.random()
        for prob, edge in probList:
            if prob[0] < rand < prob[1]:
                path = edge
                break
        return path;

    def generateProbability(self,ant):
        visitedNum = 0
        visitedTotalWeight = 0
        sample = []
        sampleSize = 0
        for edge in self.edges:
            if edge.otherNode(self).tag not in ant.visited:
                if edge.weight > 0:
                    visitedNum += 1
                    visitedTotalWeight += edge.weight
                sample.append(edge)
                sampleSize += 1
        return self.finalProbability(sample,sampleSize,visitedTotalWeight,visitedNum)

    def finalProbability(self,sample,sampleSize,totalWeight,visitNum):
        upper = 0
        for edge in sample:
            base = upper
            if edge.weight > 0:
                prob = (edge.weight / totalWeight)  * (visitNum / sampleSize)
            else:
                prob = (1 / sampleSize)
            upper = base+prob
            yield [[base,upper],edge]

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
        self.nodes = []
        self.edges = []
        self.edgeDict = {}
        self.solution = None
        self.edgesCreated = False

        self.popSize = populationSize
        self.startNode = None
        self.nodeCounter = 0

    # add nodes to list when needed
    def addNode(self,*points):
        for pos in points:
            self.nodes.append(Node(self.nodeCounter,pos))
            self.nodeCounter += 1

    def randomNode(self):
        return random.choice(self.nodes)

    def findEdgeBetweenNodes(self,tag1,tag2):
        order = intJoin(*sorted([tag1,tag2]))
        return self.edgeDict[order]

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
        if self.edgesCreated == False:
            self.generateEdges()
            self.edgesCreated = True
        for i in range(self.popSize):
            self.ant.tour(None)

class Ant():
    def __init__(self,parent):
        self.parent = parent
        self.location = None;
        self.start = None
        self.visited = []
        self.usedEdges = []
        self.longestTrip = None
        self.shortestTrip = None

        self.distance = 0

    def updateStats(self):
        if self.longestTrip == None and self.shortestTrip == None:
            self.longestTrip = self.distance
            self.shortestTrip = [self.distance,self.visited]
        elif self.longestTrip < self.distance:
            self.longestTrip = self.distance
        elif self.shortestTrip[0] > self.distance:
            self.shortestTrip = [self.distance,self.visited]
            self.parent.solution = self.shortestTrip

    def tour(self,start,report=False):
        self.location = start
        self.distance = 0
        self.visited = []
        self.usedEdges = []
        if start == None:
            self.location = self.parent.randomNode()
        self.start = self.location
        self.visitNode(self.location)

        for i in range(self.parent.nodeCounter-1):
            path = self.location.preferredPath(self)
            self.usedEdges.append(path)
            self.distance += path.length
            self.location = path.travelOn(self.location)
            self.visitNode(self.location)

        path = self.parent.findEdgeBetweenNodes(self.location.tag,self.start.tag)
        self.distance += path.length
        self.location = path.travelOn(self.location)
        self.visitNode(self.location)

        pathWeight = determineEdgeValue(self.distance,self.parent.nodeCounter)
        for edge in self.usedEdges:
            edge.weight += pathWeight

        self.updateStats()

        if report == True:
            return [self.distance,self.visited]
        return 0

    def visitNode(self,node):
        self.visited.append(node.tag)

if __name__ in '__main__':
    s = time.time()
    c = AntColony(1000)
    c.addNode(*generatePoints(7,25,324))
    c.generateEdges()

    home = c.nodes[0]

    c.runPopulation()

    finalDist, finalPath = c.finalTour(home)

    print("Distance Diffrence: ", round((c.ant.longestTrip-finalDist)/c.ant.longestTrip*100,2),"%")
    print("Final Path: ",finalPath)
    print('Took: %s seconds'%round(time.time()-s,2))
