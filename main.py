from RoutePlotter import RouteController
from tkinter import *


class App(Tk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class OptionSelector(Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.size = [self['width'],self['height']]

        self.options = []

        self.list = Listbox(self,selectmode=MULTIPLE)
        self.list.pack(expand=YES,fill=BOTH)

    # PACK and UNPACK methods

    def addItems(self,*items):
        for item in items:
            self.options.append(item)
            self.list.insert(END,item)
    # UPDATE method

    def updateList(self):
        pass

    # READ all chosen items

a = App()
a.geometry("500x500")
o = OptionSelector(a,width=500,height=500)
o.pack()

o.addItems("Ben","Ryan","Evan","Mitch")

# # Taking a list 'x' with the items
# # as languages
# x = ["C", "C++", "Java", "Python", "R",
#      "Go", "Ruby", "JavaScript", "Swift"]
#
# for each_item in range(len(x)):
#
#     list.insert(END, x[each_item])
#
#     # coloring alternative lines of listbox
#     list.itemconfig(each_item,
#              bg = "yellow" if each_item % 2 == 0 else "cyan")
#
# window.mainloop()
a.mainloop()
