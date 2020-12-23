from RoutePlotter import RouteController as SotRoute
import RealVisualizer
import string
alpha = string.ascii_lowercase

class MapVisualizer(RealVisualizer.Visualizer):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def labelNodes(self,names): ## TODO: fix this method
        r = 8
        for i, node in enumerate(self.nodes):
            pos = self.scalePoint(node)
            color = '#000'
            fill = self.cnv['bg']
            if "Outpost" in names[i]:
                color = '#f00'
            point = self.cnv.create_oval(pos[0]-r,pos[1]-r,pos[0]+r,pos[1]+r,fill='#b47346',outline='#b47346')
            n = self.cnv.create_text(pos[0],pos[1],text=names[i],font=('Arial',18),fill=color)
            bg = self.cnv.create_rectangle(self.cnv.bbox(n),fill=fill,outline=fill)
            self.cnv.tag_lower(bg,n)
            self.cnv.tag_lower(point,n)

    def drawLines(self,color='#b47346'):
        x = int(visual.closeToOrigin[0]);
        pos = visual.closeToOrigin
        while pos[0]+visual.unitSize[0] < W-visual.margin:
            pos = visual.scalePoint([x,0])
            visual.cnv.create_line(pos[0],0,pos[0],H,fill=color)
            if x >= 26:
                break
            visual.cnv.create_text(pos[0]+visual.unitSize[0]/2,15,text=alpha[x].upper(),font=("Arial",20),fill='#000')
            x+=1;
        pos = visual.scalePoint([x,0])
        visual.cnv.create_line(pos[0],0,pos[0],H,fill=color)

        y = int(visual.closeToOrigin[1]);
        pos = visual.closeToOrigin
        while pos[1]+visual.unitSize[1] < H-visual.margin:
            pos = visual.scalePoint([0,y])
            visual.cnv.create_line(0,pos[1],W,pos[1],fill=color)
            if y >= 26:
                break;
            visual.cnv.create_text(15,pos[1]+visual.unitSize[1]/2,text=y,font=("Arial",20),fill='#000')
            y += 1;
        pos = visual.scalePoint([0,y])
        visual.cnv.create_line(0,pos[1],W,pos[1],fill=color)


W, H = 1440,800
margin = 110

iterations = 1000
outposts = 2

plotter = SotRoute(iterations,NumOfOutposts=outposts)
visual = MapVisualizer((W,H),margin)

plotter.addIsland(
    "Marauder's Arch",
    "Mermaid's Hideaway",
    "The Forsaken Brink",
    "Roaring Traders",
    "Ashen Reaches",
    "Thieves' Haven",
    "Snake Island",
    "Barnacle Cay",
    "Crook's Hollow",
    # "Cinder Islet",
    # "Flame's End",
    # "Booty Isle",
    # "Paradise Spring",
    # "Shark Bait Cove",
    # "Discovery Ridge",
    # "Plunder Valley",
    # "Shipwreck Bay",
    # "Kraken's Fall",
    # "The Crooked Masts"
)
plotter.calculateRoute()
visual.insertNodeSet(*plotter.ACO.nodes)
visual.cnv['bg'] = '#d6a26a'
visual.title("Sea of Thieves Route Plotter")
names = list(plotter.islandDict.values())

visual.drawLines()

visual.connectTheDots(plotter.solution)
visual.labelNodes(names)

visual.mainloop()
