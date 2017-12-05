from Tkinter import *
import ttk
import pdb


class WidgetTreeViewTk:
    def __init__(self, parent):
        self.treeView = ttk.Treeview(parent)

        self.treeView.pack(side = LEFT)
        self.openDirectory()
        self.listOfDevices = {}
 
    def clickHandler(self, event):
        print self.treeView.focus()
 

    def openDirectory(self, listOfDevices):

        self.listOfDevices = listOfDevices

        parent = self.treeView.insert("","end", "widgets", text="inicial" )
        self.treeView.insert(parent,0, "child1", text="child" )
        self.treeView.tag_configure('ttk', background='yellow')
        self.treeView.bind("<<TreeviewSelect>>", self.clickHandler)
