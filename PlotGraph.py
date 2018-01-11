import pdb

from Tkinter import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Plot class
# Responsible for 
class PlotGraph:

    def __init__(self, parentWindow):
        self.mainWindow = parentWindow
        
        ## Input file name just beng used for debug sake
        self.figure = Figure(dpi=100)
        self.subPlot = self.figure.add_subplot(111) # returns the axes

        # create rectangle patch to be used during zooms
        # leave it hidden and only set visible during zoom procedures
        self.zoomRectangle = self.subPlot.add_patch(patches.Rectangle( (0, 0), 1.0, 1.0,
            fill=False, visible=False, animated=False, zorder=100))

        self.startX = 0
        self.startY = 0

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.figure, master=parentWindow)
        self.canvas.mpl_connect("pick_event", self.pickHandler)
        self.canvas.mpl_connect("motion_notify_event", self.motionHandler)
        self.scrollId = self.canvas.mpl_connect("scroll_event", self.scrollHandler)
        self.canvas.mpl_connect("button_press_event", self.buttonPressHandler)
        self.canvas.mpl_connect("button_release_event", self.buttonReleaseHandler)
        self.canvas.show()
        self.canvas.get_tk_widget().pack( expand=1)
    
    def enableData(self, enabledArray):
        self.subPlot.cla()
        self.zoomRectangle = self.subPlot.add_patch(patches.Rectangle( (0, 0), 1.0, 1.0,
            fill=False, visible=False, animated=False, zorder=100))

        xArray = np.array([])
        listToPlotX = []
        listToPlotY = []
        for name in enabledArray:
            if name in self.dataList:
                data = self.dataList[name]
                listToPlotY.append(data.y)
                listToPlotX.append(data.x)
#                pdb.set_trace()
                xArray = np.concatenate((xArray, data.x))
                #self.subPlot.plot(data.x, data.y,linewidth=0.5, picker=True)

        xArray = np.unique(xArray)
        xArray = np.sort(xArray)

        for index,array in enumerate(listToPlotY):
            listToPlotY[index] = np.interp(xArray, listToPlotX[index], listToPlotY[index])

        if len(listToPlotY) > 0:
            self.subPlot.stackplot(xArray, *listToPlotY, baseline="zero", linewidth=0.0, picker=True)
#        X = np.arange(0, 10, 1) 
#        Y = X + 5 * np.random.random((5, X.size))
#        self.subPlot.stackplot(X, *Y)

        self.canvas.draw()

    def setData(self, dataList):
        self.dataList = dataList

    def motionHandler(self, mouseEvent):
        print "motion {0}, {1}".format(mouseEvent.xdata, mouseEvent.ydata)

        if self.startX:
            self.zoomRectangle.set_width(mouseEvent.xdata - self.startX)
            self.zoomRectangle.set_height(mouseEvent.ydata - self.startY)

            self.canvas.draw()

    def scrollHandler(self, mouseEvent):
        print "scroll {0}, {1}, steps {2}".format(mouseEvent.xdata, mouseEvent.ydata, mouseEvent.step)
        zoomInRatio  = 0.9
        zoomOutRatio = 1.1

        xlim = self.subPlot.get_xlim()
        ylim = self.subPlot.get_ylim()

        currX = mouseEvent.xdata
        currY = mouseEvent.ydata

        distXLow  = currX-xlim[0]
        distXHigh = xlim[1]-currX
        distYLow  = currY-ylim[0]
        distYHigh = ylim[1]-currY

        if(mouseEvent.step<0):
            distXLow  *= zoomOutRatio
            distXHigh *= zoomOutRatio
            distYLow  *= zoomOutRatio
            distYHigh *= zoomOutRatio

        else:
            distXLow  *= zoomInRatio
            distXHigh *= zoomInRatio
            distYLow  *= zoomInRatio
            distYHigh *= zoomInRatio

        xlim = (currX- distXLow, currX+distXHigh )
        ylim = (currY- distYLow, currY+distYHigh )

        self.subPlot.set_xlim(xlim)
        self.subPlot.set_ylim(ylim)
        self.canvas.draw()

    def buttonPressHandler(self, mouseEvent):
        self.startX = mouseEvent.xdata
        self.startY = mouseEvent.ydata

        self.mainWindow.config(cursor="cross")

        self.zoomRectangle.set_visible(True)
        self.zoomRectangle.set_x(self.startX)
        self.zoomRectangle.set_y(self.startY)

        print "press {0}, {1}".format(mouseEvent.xdata, mouseEvent.ydata)

    def buttonReleaseHandler(self, mouseEvent):
        print "release {0}, {1}".format(mouseEvent.xdata, mouseEvent.ydata)

        startX = min(self.startX, mouseEvent.xdata)
        startY = min(self.startY, mouseEvent.ydata)

        endX = max(self.startX, mouseEvent.xdata)
        endY = max(self.startY, mouseEvent.ydata)

        self.subPlot.set_xlim([startX, endX])
        self.subPlot.set_ylim([startY, endY])

        #stop displaying the zoom rectangle
        self.zoomRectangle.set_visible(False)

        self.canvas.draw()
        self.mainWindow.config(cursor="arrow")

    def pickHandler(self, mouseEvent):
        print "pick handler"
