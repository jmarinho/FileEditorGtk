from Tkinter import *
import ttk
import pdb


class WidgetTreeViewTk:
    def __init__(self, parent):
        self.treeView = ttk.Treeview(parent )

        self.testIcon = PhotoImage(file="icons/gears.gif")
        self.treeView.pack(side = LEFT, expand = 1,fill=BOTH )

 
    def clickHandler(self, event):
        print self.treeView.focus()
 

    def childEntry(self, parent, currentLevel):

        for elem in currentLevel:

            currentNode =  self.treeView.insert(parent, 0, parent+"/"+elem['name'], text=elem['name'], image=self.testIcon, open = 1 )
            if elem['type'] == 'container':
                self.childEntry(currentNode, elem['child'])

    # listOfDevices contains a thieranrchy of dictionaries
    # which represent the platform organization
    def openDirectory(self, listOfDevices = {}):

        self.childEntry("", listOfDevices)
        self.treeView.bind("<<TreeviewSelect>>", self.clickHandler)
