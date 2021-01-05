import AntColonization

class Testing:
    def __init__(self,trials):
        self.trials = trials
        self.aco = None
        self.data = []

    def run(self,nodes):
        for i in range(self.trials):
            self.aco.reset()
            self.aco.addNode(*AntColonization.generatePoints(nodes,25,0))
            self.aco.generateEdges()
            self.aco.runPopulation()
            self.data.append(self.aco.log())
            print("%s of %s trials completed..."%(i+1,self.trials))

    def analysis(self):
        final = {}
        headings = self.data[0].keys()
        for heading in headings:
            avg = sum([runData[heading] for runData in self.data])/self.trials
            final[heading] = avg

        return final

    def displayResults(self,results):
        print("Data Points: %i"%results['points'])
        print("Number Of Ants: %i"%results['ants'])
        print("Shortest Path Found: %.2f units"%results['solution'])
        print("Path Improvement: %.2f%s"%((results['worst']-results['solution'])/results['worst']*100,"%"))
        print("Completed In: %.4f seconds"%results['time'])


test = Testing(15)
test.aco = AntColonization.AntColony(1000)
test.run(nodes=30)
test.displayResults(test.analysis())
