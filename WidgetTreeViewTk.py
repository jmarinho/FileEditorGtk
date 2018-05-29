from Tkinter import *
import ttk
import pdb


class WidgetTreeViewTk:
    def __init__(self, parent):
        self.treeView = ttk.Treeview(parent.graphFrame )


        self.icons = { "processing_unit": PhotoImage(file="icons/cogs.gif").subsample(2,2),
                       "container":       PhotoImage(file="icons/box.gif").subsample(2,2),
                       "platform":        PhotoImage(file="icons/platform.gif").subsample(2,2),
                       "component":       PhotoImage(file="icons/component.gif").subsample(2,2)}

        self.treeView.pack(side = LEFT, expand = 1,fill=BOTH )

        self.callbackParent = parent
 
    def clickHandler(self, event):
        self.callbackParent.reportNewObject(self.treeView.focus())

    def childEntry(self, parent, currentLevel):

        for elem in currentLevel:

            currentNode =  self.treeView.insert(parent, 0, parent+"/"+elem['name'], text=elem['name'], image=self.icons[elem['type']], open = 1 )
            if elem['type'] == 'container' or elem['type'] == "platform":
                self.childEntry(currentNode, elem['child'])

    # listOfDevices contains a hierarchy of dictionaries
    # which represent the platform organization
    def openDirectory(self, listOfDevices = {}):

        # Dirty hack to get the platform element display to conform
        listOfDevices[0]['type'] = "platform"
        # end of hack

        self.childEntry("", listOfDevices)
        self.treeView.bind("<<TreeviewSelect>>", self.clickHandler)

    def clear(self):
        self.treeView.delete(*self.treeView.get_children())
