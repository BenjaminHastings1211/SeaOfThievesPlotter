from RoutePlotter import RouteController as SotRoute
from MapVisualizer import MapVisualizer as Visualizer
from tkinter import *
import time

#colors
#

VERSION = 1.0

ITERATIONS = 10000
MAX_W,MAX_H = 1440,800 # screen size

class MapInteraction():
    def __init__(self,**kwargs):
        self.mapSize = kwargs['size']
        self.margin = kwargs['margin']
        self.plotter = SotRoute(kwargs['iterations'])
        self.map = None

    def generateSolution(self,outposts=1):
        self.map = Visualizer(self.mapSize,self.margin)
        self.plotter.outpostNum = outposts
        resp = self.plotter.calculateRoute()
        self.map.insertNodeSet(*self.plotter.ACO.nodes)
        self.map.cnv['bg'] = '#d6a26a'
        self.map.title("Route")
        names = list(self.plotter.islandDict.values())
        self.map.drawLines()
        self.map.connectTheDots(resp[1])
        self.map.labelNodes(names)
        self.map.update()
        self.map.update_idletasks()

    def reset(self):
        self.plotter.reset()

# class TextInput(Frame):
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#
#     def setup(self,**k)

class App(Tk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.map = MapInteraction(iterations=ITERATIONS,size=(MAX_W,MAX_H),margin=110)

        self.titleFrame = Frame(self,bg='#d6a26a')
        self.titleFrame.pack(side=TOP,fill=BOTH)
        Label(self.titleFrame,text="Sea Of Thieves Route Planner",font=("Arial",36),bg=self.titleFrame['bg']).pack()
        Label(self.titleFrame,text="Version %s"%VERSION,font=("Arial",14),bg=self.titleFrame['bg']).pack()

        self.content = Frame(self,bg='orange')
        self.content.pack(side=BOTTOM,fill=BOTH)

        self.options = SearchField(self.content,width=300,height=500)
        self.options.pack(side=LEFT)
        self.options.pack_propagate(0)

        Button(self.content,text='Calculate Route',command=self._handleSubmit,font=("Arial",24)).pack(side=BOTTOM,padx=10,pady=10,fill=X)


    def _handleSubmit(self):
        self.map.reset()
        self.map.plotter.addIsland(*self.options.readSelected())
        self.map.generateSolution(2)

class SearchField(Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.size = [self['width'],self['height']]
        self['bg'] = 'red'
        self.options = []

        self.entry = Entry(self,font=("Arial",18))
        self.entry.pack(fill=BOTH,side=TOP)
        mid = Frame(self)
        mid.pack(expand=YES,fill=BOTH)
        self.list = Listbox(mid,selectmode=MULTIPLE,font=('Arial',18))
        self.list.pack(side=LEFT,fill=BOTH,expand=YES)
        scrollbar = Scrollbar(mid)
        scrollbar.pack(side = RIGHT, fill = BOTH)
        self.list.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = self.list.yview)

        self.clear = Button(self,text='Deselect All',font=("Arial",18),command=lambda : self.list.selection_clear(0,END))
        self.clear.pack(fill=BOTH,side=BOTTOM)

    # PACK and UNPACK methods

    def addItems(self,*items):
        for item in items:
            self.options.append(item)
            self.list.insert(END,item)
    # UPDATE method

    def updateList(self):
        pass

    # READ all chosen items

    def readSelected(self):
        return [self.list.get(i) for i in self.list.curselection()]



a = App()
a.geometry("700x500")
a.title("Sea Of Thieves Route Planner")

e = sorted(list(a.map.plotter.mapData['islands'].keys()))
a.options.addItems(*e)

# a.mainloop()


while 1:
    # o.readSelected()
    a.update()
    a.update_idletasks()
    time.sleep(0.01)
