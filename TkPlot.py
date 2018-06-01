import json
import pdb
import PlotGraph
import WidgetTreeViewTk 
from string import *
from Tkinter import *
import ttk
import numpy as np
import os
import tkFileDialog

class Data:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        
        self.dataXRange = [float(min(self.x)), float(max(self.x))]
        self.dataYRange = [float(min(self.y)), float(max(self.y))]

class WrapperGraph(Frame):

    def openFileDialog(self):
        fileName = tkFileDialog.askopenfilename(initialdir = "output",title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))

        nameList, dataList = self.openFile(fileName) 
        self.graph.setData(nameList, dataList)

    def __init__(self, mainWindow):

        self.colorList = []
        self.mainWindow = mainWindow

        menu = Menu(mainWindow)
        fileList = Menu(menu)

        dropDownList = menu.add_command(label="Open file dialog", command= self.openFileDialog)

        mainWin.config(menu=menu)

        self.graphFrame = Frame(mainWindow)
        self.graphFrame.pack(expand=0)
        self.TreeSelector = WidgetTreeViewTk.WidgetTreeViewTk(self)

        self.mainNote = ttk.Notebook(self.graphFrame, style ="BW.TLabel")
        self.mainNote.pack(fill=BOTH, expand=1) 

        # Create the several graph 
        self.frame1 = ttk.Labelframe(self.mainNote, text='Power', width=100, height=100)

        self.frame2 = ttk.Labelframe(self.mainNote, text='Advanced Plot', width=100, height=100)
        self.mainNote.add(self.frame1, text="power")
        self.mainNote.add(self.frame2, text="Advanced Plot")
        self.frame2 = ttk.Frame(self.mainNote)
        self.mainNote.insert("end", self.frame2)

        self.graph = PlotGraph.PlotGraph(self.frame1)
        
        self.toggleFrame = Frame(self.graphFrame, width=25, height=10)
        self.toggleFrame.grid_propagate(0)
        self.toggleFrame.pack(fill=X, expand=1)

        self.graph.handleResize()

    def openFile(self, json_file_name):

        inputData = json.load(open(json_file_name, "r"))

        self.TreeSelector.clear()
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
