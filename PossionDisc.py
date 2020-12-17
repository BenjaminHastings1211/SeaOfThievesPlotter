
import math, random

class PossionDiscSampling():
    def __init__(self,r,k=30):
        self.r = r
        self.k = k
        self.bounds = []

        self.domain = []
        self.activeList = []
        self.cellSize = round(r / math.sqrt(2),2)
        self.points = []

    def reset(self):
        self.domain = []
        self.defineGrid()
        self.activeList = []
        self.points = []

    def defineGrid(self,existing=None):
        if existing != None:
            self.bounds = [int(existing[0]/self.cellSize),int(existing[1]/self.cellSize)]
        for y in range(self.bounds[1]):
            row = []
            for x in range(self.bounds[0]):
                row.append(Cell())
            self.domain.append(row)

    def validatePoint(self,pos):
        xO, yO = self.getCell(pos,True)
        for y in range(yO-1,yO+2):
            for x in range(xO-1,xO+2):
                if ((0 <= x <= self.bounds[0]) and (0 <= y <= self.bounds[1])) == False:
                    return False
                try:
                    cell = self.domain[y][x]
                    if cell.point != None:
                        return False
                except IndexError:
                    continue
        return True

    def getCell(self,pos,giveIndex=False):
        index = [int(val/self.cellSize) for val in pos]
        if giveIndex == True:
            return index
        return self.domain[index[1]][index[0]]

    def iterate(self):
        for i in range(len(self.activeList),0,-1):
            active = self.activeList[i-1]
            found = False
            for testPoint in active.generatePossiblePoints(self.r,self.k):
                if self.validatePoint(testPoint):
                    cell = self.getCell(testPoint)
                    cell.point = testPoint
                    self.points.append(cell.point)
                    self.activeList.append(cell)
                    found = True
            if found == False:
                del self.activeList[i-1]

    def createPoints(self):
        if len(self.activeList) == 0:
            self.insertPoint((random.randint(0,int(self.bounds[0]*self.cellSize)),random.randint(0,int(self.bounds[1]*self.cellSize))))
        while len(self.activeList) > 0:
            self.iterate();

    def insertPoint(self,pos):
        cell = self.getCell(pos)
        cell.point = pos
        self.activeList.append(cell)
        self.points.append(pos)

class Cell():
    def __init__(self):
        self.point = None #None if no point is present, coords if point is present

    def generatePossiblePoints(self,radius,iterations):
        for i in range(iterations):
            dist = random.randint(radius,radius*2)
            angle = random.randint(0,360)
            x = int(math.cos(angle)*dist) + self.point[0]
            y = int(math.sin(angle)*dist) + self.point[1]
            yield [x,y]


if __name__ in "__main__":
    sampling = PossionDiscSampling(50,20)
    sampling.defineGrid((500,500))
    sampling.insertPoint((250,250))

    sampling.createPoints()

    print('Done')
