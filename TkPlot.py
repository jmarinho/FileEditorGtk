import json
import pdb

import PlotGraph
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

        graphFrame = Frame(mainWindow)
        graphFrame.pack()
        self.nameList, self.dataList = self.openFile("plotInput.json") 
        self.graph = PlotGraph.PlotGraph(graphFrame)
        self.graph.setData(self.dataList)

        toggleFrame = Frame(graphFrame)
        toggleFrame.pack()

        self.buttonList = []
        self.checkerArray = {}
        index = 0
        for nameElem in self.nameList:
            self.checkerArray[nameElem] = IntVar()
            self.buttonList.append(Checkbutton(toggleFrame, text=nameElem,
                command=self.handleToggle, variable=self.checkerArray[nameElem], offvalue=0, onvalue=1))
            self.buttonList[-1].grid(column=index, row=1)
            index += 1

        self.handleToggle()

    def openFile(self, json_file_name):

        inputData = json.load(open(json_file_name, "r"))

        componentNames = inputData["traces"].keys()

        dataList ={} 
        nameList = []
        for components in componentNames:
            
            data = sorted(inputData["traces"][components]["total_power"].items(), key = self.tupleToFloatArray)

            dataLen = len(data)
            x = [0]*dataLen
            y = [0]*dataLen

            for index,item in enumerate(data):
                x[index] = item[0]
                y[index] = item[1]

            dataList[components] = Data(components, x, y)
            nameList.append(components)
            
        return nameList, dataList

    def tupleToFloatArray(self, tupleVariable):
        return float(tupleVariable[0])

    def updateToggleArray(self, nameList):
        self.graph.enableData(nameList)

    def handleToggle(self):
        enabledNames = []
        for name, val in self.checkerArray.items():
            if val.get() == 1:
                enabledNames.append(name)
        self.graph.enableData(enabledNames)            

mainWin = Tk()

graph = WrapperGraph(mainWin)

mainWin.geometry('651x700+51+51')
mainWin.wm_title('')

mainWin.mainloop()



