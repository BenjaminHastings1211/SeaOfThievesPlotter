from tkinter import *
import random,time
import AntColonization

W,H = 600,600

def mapVal(s,a1,a2,b1,b2):
    return b1 + ((s - a1)*(b2-b1))/(a2-a1);

class AntColony(AntColonization.AntColony):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def addVisualNode(self,*points):
        for pos in points:
            if self.nodeCounter == 0: # does this even matter ????
                self.home = Node(self.nodeCounter,pos)
                self.nodes.append(self.home)
            else:
                self.nodes.append(Node(self.nodeCounter,pos))
            self.nodeCounter += 1

    # create all edges connecting the nodes
    def generateVisualEdges(self):
        count = 0
        for first in range(0,self.nodeCounter-1):
            for second in range(first+1,self.nodeCounter):
                edge = Edge(count,self.nodes[first],self.nodes[second])
                self.edges.append(edge)
                self.edgeDict[AntColonization.intJoin(first,second)] = edge
                count += 1

    def displayPath(self,route,color='#000'):
        for i, node in enumerate(route):
            next = route[i+1]
            path = self.findEdgeBetweenNodes(node,next)
            path.setState('normal')
            path.setColor(color)
            if next == route[0]:
                break

    def hideAll(self):
        for edge in self.edges:
            edge.setState('hidden')

class Edge(AntColonization.Edge):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.obj = app.screen.create_line(self.nodes[0].pos[0],self.nodes[0].pos[1],self.nodes[1].pos[0],self.nodes[1].pos[1],width=0)

    def setState(self,state):
        app.screen.itemconfig(self.obj,state=state)

    def setColor(self,color):
        app.screen.itemconfig(self.obj,fill=color)

class Node(AntColonization.Node):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        color = "#f33"

        self.obj = app.screen.create_text(self.pos[0],self.pos[1],text=self.tag,font=('Arial',48),fill=color)


class Window(Tk):
    def __init__(self,size,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.size = size
        self.geometry("%sx%s"%(size[0],size[1]))

        self.screen = Canvas(self,width=size[0],height=size[1],bd=0,highlightthickness=0,bg='white')
        self.screen.pack()

def generatePoints(num,margin,seed=0):
    random.seed(seed)
    points = []
    for i in range(num):
        points.append((random.randint(margin,W-margin),random.randint(margin,H-margin)))

    random.seed(time.time())
    return points

seed = random.randint(-1000,1000)
seed = 15
print("seed: ",seed)

app = Window([W,H])
s = time.time()
nodes = 20

colony = AntColony(50000)

colony.addVisualNode(*generatePoints(nodes,25,seed))
colony.generateVisualEdges()

start = colony.nodes[0]

dist,path = colony.ant.tour(start,False,report=True)

colony.runPopulation()

finalDist, finalPath = colony.ant.tour(start,True,report=True)

colony.hideAll()
print('Original Tour Length: %s'%(round(dist,2)))
print('Final Tour Length: %s'%(round(finalDist,2)))
print('Shortened By: ' + str(round((dist-finalDist)/dist * 100,2)) + '%')
print(finalPath)
colony.displayPath(finalPath,'black')

print('Took: %s seconds'%round(time.time()-s,2))
app.mainloop()
