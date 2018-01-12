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
       
        self.annot = [] 
    
    def enableData(self, enabledArray):
        self.subPlot.cla()
        self.zoomRectangle = self.subPlot.add_patch(patches.Rectangle( (0, 0), 1.0, 1.0,
            fill=False, visible=False, animated=False, zorder=100))

        xArray = np.array([])
        self.listToPlotX = []
        self.listToPlotY = []
        for name in enabledArray:
            if name in self.dataList:
                data = self.dataList[name]
                self.listToPlotY.append(data.y)
                self.listToPlotX.append(data.x)
                xArray = np.concatenate((xArray, data.x))


        xArray = np.unique(xArray)
        xArray = np.sort(xArray)

        localListToPlotY = []
        for index,array in enumerate(self.listToPlotY):
            localListToPlotY.append( np.interp(xArray, self.listToPlotX[index], self.listToPlotY[index]))

        if len(self.listToPlotY) > 0:

            self.subPlot.stackplot(xArray, *localListToPlotY, baseline="zero", linewidth=0.0, picker=True)
            bbox_props = dict(fc="white", ec="b", lw=0.1)
            self.annot = self.subPlot.annotate("bla", bbox = bbox_props, fontsize=8, xy=(0,0), xytext=(0,0),textcoords="offset points")

        self.canvas.draw_idle()

    def setData(self, dataList):
        self.dataList = dataList

    def getAnotString(self, xCoord):
        returnString = ""
        for elemX, elemY in zip(self.listToPlotX, self.listToPlotY):
            returnString += "{:.4f}".format(np.interp(xCoord, elemX, elemY))+"\n"
        return returnString

    def motionHandler(self, mouseEvent):
        print "motion {0}, {1}".format(mouseEvent.xdata, mouseEvent.ydata)

        if self.startX:

            self.zoomRectangle.set_width(mouseEvent.xdata - self.startX)
            self.zoomRectangle.set_height(mouseEvent.ydata - self.startY)

            self.canvas.draw_idle()

        elif self.annot and mouseEvent.xdata and  mouseEvent.ydata:
            print "change annotation"

            self.annot.xy = (mouseEvent.xdata, 0)#mouseEvent.ydata)
            self.annot.set_text(self.getAnotString(mouseEvent.xdata))
            self.annot.set_visible(True)
            self.canvas.draw_idle()

    def scrollHandler(self, mouseEvent):
        #print "scroll {0}, {1}, steps {2}".format(mouseEvent.xdata, mouseEvent.ydata, mouseEvent.step)
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
#        pdb.set_trace()
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
        self.startX = []
    def pickHandler(self, mouseEvent):
        print "pick handler"
