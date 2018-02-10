import json
import pdb
import PlotGraph
import WidgetTreeViewTk 
from string import *
from Tkinter import *
import ttk
import numpy as np

class Data:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        
        self.dataXRange = [float(min(self.x)), float(max(self.x))]
        self.dataYRange = [float(min(self.y)), float(max(self.y))]

class WrapperGraph(Frame):

    def __init__(self, mainWindow):
        self.colorList = []
        self.mainWindow = mainWindow

        self.graphFrame = Frame(mainWindow)
        self.graphFrame.pack(expand=1)
        self.TreeSelector = WidgetTreeViewTk.WidgetTreeViewTk(self)
        self.nameList, self.dataList = self.openFile("plotInput.json") 
        self.subNameList = []
        self.graph = PlotGraph.PlotGraph(self.graphFrame)
        self.graph.setData(self.dataList)

        self.toggleFrame = Frame(self.graphFrame)
        self.toggleFrame.pack(expand=1)

        self.buttonList = []

        self.handleResize()
       
    def handleResize(self):
        print "RESIZE"
        self.checkerArray = {}
        
        for button in self.buttonList:
            button.grid_forget()
 
        self.buttonList = []

        index = 0
        for nameElem in self.subNameList:
            color = self.colorList[index]
            R = "{:02X}".format(int(color[0] * 255.0))
            G = "{:02X}".format(int(color[1] * 255.0))
            B = "{:02X}".format(int(color[2] * 255.0))
            index += 1
            self.checkerArray[nameElem] = IntVar()
            self.buttonList.append(Checkbutton(self.toggleFrame, text=split(nameElem,"/")[-1],
                command=self.handleToggle, variable=self.checkerArray[nameElem], offvalue=0, onvalue=1,
                selectcolor="#"+R+G+B))
            
            self.buttonList[-1].toggle()

        indexR = 0
        indexC = 0
        for button in self.buttonList:
            button.grid(sticky = 'W', row = indexR, column = indexC)
            indexC += 1
            button.update()
            
            #print button.winfo_width()
            if( indexC>3):
                indexC = 0
                indexR += 1


        self.handleToggle()

    def openFile(self, json_file_name):

        inputData = json.load(open(json_file_name, "r"))

        self.TreeSelector.openDirectory([inputData['platform']])

        componentNames = inputData["traces"].keys()

        dataList = {} 
        nameList = []
        for components in componentNames:
            
            data = sorted(inputData["traces"][components]["total_power"].items(), key = self.tupleToFloatArray)

            dataLen = len(data)
            x = [0]*dataLen
            y = [0]*dataLen

            for index,item in enumerate(data):
                x[index] = float(item[0])
                y[index] = float(item[1])

            dataList[components] = Data(components, x, y)
            nameList.append(components)
            
        return nameList, dataList

    def tupleToFloatArray(self, tupleVariable):
        return float(tupleVariable[0])

    def reportNewObject(self, name):
        self.subNameList = [subElem for subElem in self.nameList if name in subElem and name != subElem ]

        self.colorList = []
        nameListLen = len(self.subNameList)
        if nameListLen == 0:
            self.subNameList = [name]
            self.colorList = [(0,0,1)]
        else:
            self.colorList = [(1.0-x,x/2,x) for x in np.arange(0.1,1, 0.9/nameListLen)]

        self.updateToggleArray(self.subNameList, self.colorList)
        self.handleResize()
 
    def updateToggleArray(self, nameList, colorList):
        self.graph.enableData(nameList, self.colorList)

    def handleToggle(self):
        enabledNames = []
        partialColorList = []
        index = 0
        for name, val in self.checkerArray.items():
            if val.get() == 1:
                enabledNames.append(name)
                partialColorList.append(self.colorList[index])
            index += 1

        self.graph.enableData(enabledNames, partialColorList)

# Create Main Window
mainWin = Tk()

# The widget that wraps the main plotting widget,
# plot selection buttons and tree element selection

mainWin.geometry("{0}x{1}+0+0".format(mainWin.winfo_screenwidth(), mainWin.winfo_screenheight()))
mainWin.wm_title('')

graph = WrapperGraph(mainWin)
mainWin.mainloop()
