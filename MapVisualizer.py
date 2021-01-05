import GraphVisualizer
import string

class MapVisualizer(GraphVisualizer.Visualizer):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.alpha = string.ascii_lowercase

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
        W,H = 1440,900
        x = int(self.closeToOrigin[0]);
        pos = self.closeToOrigin
        while pos[0]+self.unitSize[0] < W-self.margin:
            pos = self.scalePoint([x,0])
            self.cnv.create_line(pos[0],0,pos[0],H,fill=color)
            if x >= 26:
                break
            self.cnv.create_text(pos[0]+self.unitSize[0]/2,15,text=self.alpha[x].upper(),font=("Arial",20),fill='#000')
            x+=1;
        pos = self.scalePoint([x,0])
        self.cnv.create_line(pos[0],0,pos[0],H,fill=color)

        y = int(self.closeToOrigin[1]);
        pos = self.closeToOrigin
        while pos[1]+self.unitSize[1] < H-self.margin:
            pos = self.scalePoint([0,y])
            self.cnv.create_line(0,pos[1],W,pos[1],fill=color)
            if y >= 26:
                break;
            self.cnv.create_text(15,pos[1]+self.unitSize[1]/2,text=y,font=("Arial",20),fill='#000')
            y += 1;
        pos = self.scalePoint([0,y])
        self.cnv.create_line(0,pos[1],W,pos[1],fill=color)

if __name__ == "__main__":
    from RoutePlotter import RouteController as SotRoute

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
        "Shark Bait Cove",
        "Discovery Ridge"
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
