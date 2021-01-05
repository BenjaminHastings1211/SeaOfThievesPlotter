from tkinter import *

def mapVal(s,a1,a2,b1,b2):
    return b1 + ((s - a1)*(b2-b1))/(a2-a1);

class Visualizer(Tk):
    def __init__(self,size,margin=25,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.size = size
        self.nodes = []
        self.closeToOrigin = None
        self.farFromOrigin = None
        self.margin = margin
        self.unitSize = None

        self.cnv = Canvas(self,width=size[0],height=size[1],bd=0,highlightthickness=0)
        self.cnv.pack()

    def insertNodeSet(self,*nodes):
        self.closeToOrigin = list(nodes[0].pos)
        self.farFromOrigin = list(nodes[0].pos)

        for node in nodes:
            if node.pos[0] < self.closeToOrigin[0]:
                self.closeToOrigin[0] = node.pos[0]
            elif node.pos[0] > self.farFromOrigin[0]:
                self.farFromOrigin[0] = node.pos[0]
            if node.pos[1] < self.closeToOrigin[1]:
                self.closeToOrigin[1] = node.pos[1]
            elif node.pos[1] > self.farFromOrigin[1]:
                self.farFromOrigin[1] = node.pos[1]

            self.nodes.append(node.pos)

        x1 = self.scalePoint([1,0])[0]
        x2 = self.scalePoint([2,0])[0]
        y1 = self.scalePoint([0,1])[1]
        y2 = self.scalePoint([0,2])[1]
        self.unitSize = [x2-x1,y2-y1]

    def numberNodes(self,fontSize=48):
        for i, node in enumerate(self.nodes):
            pos = self.scalePoint(node)
            self.cnv.create_text(pos[0],pos[1],text=i,font=('Arial',fontSize),fill='red')

    def scalePoint(self,point):
        return [mapVal(val,self.closeToOrigin[i],self.farFromOrigin[i],self.margin,self.size[i]-self.margin) for i, val in enumerate(point)]

    def connectTheDots(self,orderedList):
        print(orderedList)
        for index, path in enumerate(orderedList):
            try:
                next = orderedList[index+1]
            except: break
            print(self.nodes[path])
            p1 = self.scalePoint(self.nodes[path])
            p2 = self.scalePoint(self.nodes[next])
            self.cnv.create_line(p1[0],p1[1],p2[0],p2[1],fill='black')
            # if next == orderedList[0]:
            #     break;

if __name__ in "__main__":
    import AntColonization as ACO
    from PossionDisc import PossionDiscSampling as Sampling
    margin = 25
    W,H = 600,500
    sample = Sampling(65,10,(W-margin*2,H-margin*2))
    sample.createPoints()

    aco = ACO.AntColony(10000)
    aco.addNode(*sample.points)
    aco.runPopulation()
    aco.log()

    vis = Visualizer((W,H),margin)
    vis.insertNodeSet(*aco.nodes)
    vis.connectTheDots(aco.solution[1])
    vis.numberNodes()
    vis.mainloop()
