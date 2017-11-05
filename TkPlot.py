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

class WrapperGraph:

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        dataList = self.openFile("plotInput.json") 
        self.graph = PlotGraph.PlotGraph(mainWindow)
        self.graph.setData(dataList)


    def openFile(self, json_file_name):

        inputData = json.load(open(json_file_name, "r"))

        componentNames = inputData["traces"].keys()

        dataList = []
        for components in componentNames:

            data = sorted(inputData["traces"][components]["total_power"].items(), key = self.tupleToFloatArray)

            dataLen = len(data)
            x = [0]*dataLen
            y = [0]*dataLen

            for index,item in enumerate(data):
                x[index] = item[0]
                y[index] = item[1]

            dataList.append(Data(components, x, y) )
            
        return dataList

    def tupleToFloatArray(self, tupleVariable):
        return float(tupleVariable[0])

mainWin = Tk()

graph = WrapperGraph(mainWin)

mainWin.geometry('651x700+51+51')
mainWin.wm_title('')

mainWin.mainloop()



