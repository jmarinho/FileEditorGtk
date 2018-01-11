import json
import pdb
import PlotGraph
import WidgetTreeViewTk 
from string import *
from Tkinter import *

class Data:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        
        self.dataXRange = [float(min(self.x)), float(max(self.x))]
        self.dataYRange = [float(min(self.y)), float(max(self.y))]

class WrapperGraph(Frame):

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        self.graphFrame = Frame(mainWindow)
        self.graphFrame.pack()
        self.TreeSelector = WidgetTreeViewTk.WidgetTreeViewTk(self)
        self.nameList, self.dataList = self.openFile("plotInput.json") 
        self.subNameList = []
        self.graph = PlotGraph.PlotGraph(self.graphFrame)
        self.graph.setData(self.dataList)

        self.toggleFrame = Frame(self.graphFrame)
        self.toggleFrame.pack()

        self.buttonList = []

        self.handleResize()

       
    def handleResize(self):

        self.checkerArray = {}
        
        for button in self.buttonList:
            button.grid_forget()
#            button.update()
 
        self.buttonList = []

        for nameElem in self.subNameList:
            self.checkerArray[nameElem] = IntVar()
            self.buttonList.append(Checkbutton(self.toggleFrame, text=split(nameElem,"/")[-1],
                command=self.handleToggle, variable=self.checkerArray[nameElem], offvalue=0, onvalue=1))
            
            self.buttonList[-1].toggle()

        indexR = 0
        indexC = 0
        for button in self.buttonList:
            button.grid(sticky = 'W', row = indexR, column = indexC)
            indexC += 1
            if( indexC>3):
                indexC = 0
                indexR += 1

        for button in self.buttonList:
            button.update()
            #print self.buttonList[-1].winfo_width()

        self.handleToggle()

    def openFile(self, json_file_name):

        inputData = json.load(open(json_file_name, "r"))

        self.TreeSelector.openDirectory([inputData['platform']])

        componentNames = inputData["traces"].keys()

        dataList ={} 
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
        self.subNameList = [subElem for subElem in self.nameList if name in subElem ]
        self.updateToggleArray(self.subNameList)
        self.handleResize()
 
    def updateToggleArray(self, nameList):
        self.graph.enableData(nameList)

    def handleToggle(self):
        enabledNames = []
        for name, val in self.checkerArray.items():
            if val.get() == 1:
                enabledNames.append(name)
        self.graph.enableData(enabledNames)

# Create Main Window
mainWin = Tk()

# The widget that wraps the main plotting widget,
# plot selection buttons and tree element selection
graph = WrapperGraph(mainWin)

mainWin.geometry('651x700+51+51')
mainWin.wm_title('')

mainWin.mainloop()
