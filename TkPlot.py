import json
import pdb

from Tkinter import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Plot class
# Responsible for 
class PlotGraph:

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        
        ## Input file name just beng used for debug sake
        json_file_name = "plotInput.json" 
        componentName = "/TopLevel/SoC"
        self.figure = Figure(dpi=100)
        self.subPlot = self.figure.add_subplot(111) # returns the axes

        self.dataXRange
        self.dataYXRange

        inputData = json.load(open(json_file_name, "r"))

        data = sorted(inputData["traces"][componentName]["total_power"].items(), key = self.tupleToFloatArray)

        dataLen = len(data)
        self.x = [0]*dataLen
        self.y = [0]*dataLen

        for index,item in enumerate(data):
            self.x[index] = item[0]
            self.y[index] = item[1]

        self.subPlot.plot(self.x, self.y)

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.figure, master=mainWin)
        self.canvas.mpl_connect("motion_notify_event", self.motionHandler)
        self.canvas.mpl_connect("scroll_event", self.scrollHandler)
        self.canvas.mpl_connect("button_press_event", self.buttonPressHandler)
        self.canvas.mpl_connect("button_release_event", self.buttonReleaseHandler)
        self.canvas.show()
        self.canvas.get_tk_widget().pack( expand=1)


    def tupleToFloatArray(self, tupleVariable):
        return float(tupleVariable[0])

    def motionHandler(self, mouseEvent):
        print "motion {0}+, {1}".format(mouseEvent.xdata, mouseEvent.ydata)

    def scrollHandler(self, mouseEvent):
        print "scroll {0}+, {1}".format(mouseEvent.xdata, mouseEvent.ydata)

    def buttonPressHandler(self, mouseEvent):
        self.startX = mouseEvent.xdata
        self.startY = mouseEvent.ydata
        
        print "press {0}+, {1}".format(mouseEvent.xdata, mouseEvent.ydata)

    def buttonReleaseHandler(self, mouseEvent):
        print "release {0}+, {1}".format(mouseEvent.xdata, mouseEvent.ydata)
    
        startX = min(self.startX, mouseEvent.xdata)
        startY = min(self.startY, mouseEvent.ydata)

        endX = max(self.startX, mouseEvent.xdata)
        endY = max(self.startY, mouseEvent.ydata)

        self.subPlot.set_xlim([startX, endX]) 
        self.canvas.draw()

mainWin = Tk()

graph = PlotGraph(mainWin)


mainWin.geometry('651x700+51+51')
mainWin.wm_title('')




mainWin.mainloop()



