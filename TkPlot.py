import json
import pdb
import PlotGraph
import WidgetTreeViewTk 
from string import *
from Tkinter import *
import ttk
import numpy as np

class listFiles:
    pass
    
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

        menu = Menu(mainWindow)
        fileList = Menu(menu)
        menu.add_cascade(label="Load Results", menu=fileList)
        mainWin.config(menu=menu)


        self.graphFrame = Frame(mainWindow)
        self.graphFrame.pack(expand=0)
        self.TreeSelector = WidgetTreeViewTk.WidgetTreeViewTk(self)
        self.graph = PlotGraph.PlotGraph(self.graphFrame)
        
        self.toggleFrame = Frame(self.graphFrame, width=25, height=10)
        self.toggleFrame.grid_propagate(0)
        self.toggleFrame.pack(fill=X, expand=1)

        self.graph.handleResize()

        nameList, dataList = self.openFile("plotInput.json") 
        self.graph.setData(nameList, dataList)
       
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
        self.graph.reportNewObject(name)


# Create Main Window
mainWin = Tk()

# The widget that wraps the main plotting widget,
# plot selection buttons and tree element selection

mainWin.geometry("{0}x{1}+0+0".format(mainWin.winfo_screenwidth(), mainWin.winfo_screenheight()))
mainWin.wm_title('')

graph = WrapperGraph(mainWin)
mainWin.mainloop()
