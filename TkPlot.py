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

    def __init__():
        pass
        
    ## Input file name just beng used for debug sake
    json_file_name = "plotInput.json" 
    componentName = "/TopLevel/SoC"

    def tupleToFloatArray(tupleVariable):
        return float(tupleVariable[0])

    def motionHandler(mouseEvent):
        print "{0}+, {1}".format(mouseEvent.xdata, mouseEvent.ydata)

    mainWin = Tk()

    mainWin.geometry('651x700+51+51')
    mainWin.wm_title('')


    figure = Figure(dpi=100)
    a = figure.add_subplot(111)

    inputData = json.load(open(json_file_name, "r"))

    data = sorted(inputData["traces"][componentName]["total_power"].items(), key = tupleToFloatArray)

    dataLen = len(data)
    x = [0]*dataLen
    y = [0]*dataLen

    for index,item in enumerate(data):
        x[index] = item[0]
        y[index] = item[1]


    a.plot(x,y)

    # a tk.DrawingArea
    canvas = FigureCanvasTkAgg(figure, master=mainWin)
    canvas.mpl_connect("motion_notify_event", motionHandler)
    canvas.show()
    canvas.get_tk_widget().pack( expand=1)


    mainWin.mainloop()

graph = PlotGraph()


