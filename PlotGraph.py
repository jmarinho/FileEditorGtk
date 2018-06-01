import pdb

from Tkinter import *
import ttk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import bisect
from string import *
from matplotlib.text import OffsetFrom
from matplotlib.offsetbox import  DrawingArea, AnnotationBbox, TextArea
from matplotlib import colors as mcolors

from colorList import colorPallete

# Plot class
class PlotGraph:

    def __init__(self, parentWindow):
        self.style = ttk.Style()
        self.style.configure("BW.TLabel", foreground="black", background="white")

        self.mainWindow = parentWindow

        ## Input file name just beng used for debug sake
        self.figure = Figure(figsize=(25, 25), dpi=100)
        self.subPlot = self.figure.add_subplot(111) # returns the axes

        # create rectangle patch to be used during zooms
        # leave it hidden and only set visible during zoom procedures
        self.zoomRectangle = self.subPlot.add_patch(patches.Rectangle( (0, 0), 1.0, 1.0,
            fill=False, visible=False, animated=True, zorder=100))

        self.startX = 0
        self.startY = 0

        self.subFrameCheckButtons = ttk.Frame(self.mainWindow)

        self.subFrameCheckButtons.pack(side=BOTTOM)
        self.subFrameGraph = ttk.Frame(self.mainWindow)
        self.subFrameGraph.pack()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.mainWindow)


        self.canvas.mpl_connect("pick_event", self.pickHandler)
        self.canvas.mpl_connect("motion_notify_event", self.motionHandler)
        self.scrollId = self.canvas.mpl_connect("scroll_event", self.scrollHandler)
        self.canvas.mpl_connect("button_press_event", self.buttonPressHandler)
        self.canvas.mpl_connect("button_release_event", self.buttonReleaseHandler)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(expand=1)

        self.buttonList = []
        self.subNameList = []
    
    def enableData(self, enabledArray, colorList):

        self.PartialNameList = enabledArray
        self.PartialColorList = colorList

        self.annot = [] 
        self.stackPlotData = []
        self.bboxList = []

        self.subPlot.cla()
        self.zoomRectangle = self.subPlot.add_patch(patches.Rectangle( (0, 0), 1.0, 1.0,
            fill=False, visible=False, animated=False, antialiased = False, zorder=100))

        numLines = len(enabledArray)

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

        self.xArray = xArray

        # Create functions defined at newXArray points from the prior X and Y arrays.
        # The output functions all have the same size as newXArray
        def createFuncAtX(newXArray, priorXArray, priorYArray):

            indexPrior = 0
            priorSize = len(priorXArray)

            newYArray = [0]*len(newXArray)
            #import pdb
            #pdb.set_trace()

            for indexNew, x in enumerate(newXArray):
                while x > priorXArray[indexPrior] and indexPrior < priorSize:
                    indexPrior+=1
               
                newYArray[indexNew] = priorYArray[max(indexPrior-1,0)]
            return newYArray


        self.localListToPlotY = []
        for index,array in enumerate(self.listToPlotY):
            #self.localListToPlotY.append( np.interp(xArray, self.listToPlotX[index], self.listToPlotY[index]))
            self.localListToPlotY.append( createFuncAtX(xArray, self.listToPlotX[index], self.listToPlotY[index]))

        if len(self.listToPlotY) > 0:

            self.subPlot.stackplot(xArray, *self.localListToPlotY, colors = colorList, baseline="zero", linewidth=0.0, picker=True, antialiased = False)

            self.canvas.draw()

            self.zoomXlims = self.subPlot.get_xlim() 
            self.zoomYlims = self.subPlot.get_ylim() 

        for index, elem in enumerate(self.listToPlotY):

            bbox_props = dict(fc=self.PartialColorList[index] , ec="b", lw=0.1)
            self.bboxList.append(bbox_props)

            annot = self.createBall(self.PartialColorList[index])
            self.annot.append(annot)
            self.subPlot.add_artist(annot)

        self.legend, self.legendArea = self.createLabelSquare()
        self.subPlot.add_artist(self.legendArea)

    def getPlotXLim(self):
        return self.subPlot.get_xlim()

    def getPlotYLim(self):
        return self.subPlot.get_ylim()

    # helper method to determine if a point is inside the plot
    def checkInsideDrawable(self, x, y):
        xlim = self.getPlotXLim()
        ylim = self.getPlotYLim()

        return (x>min(xlim) and x<max(xlim) and y>min(ylim) and y<max(ylim))

    def createLabelSquare(self):

        ta = TextArea("Test 1", minimumdescent=False)
        ab = AnnotationBbox(ta, xy=(0,0), xybox=(1.02, 1), 
                xycoords=("data", "axes fraction"), boxcoords=("data", "axes fraction"), box_alignment=(0,0), 
                frameon=True )
        ab.set_visible(False)

        return ta, ab

    
    def createBall(self, colour):

        radius = 2
        da = DrawingArea(radius, radius, 10, 10)
        circle = patches.Circle((0.0, 0.0), radius=radius, edgecolor='k', facecolor=colour, fill=True, ls='solid',clip_on=False)
        da.add_artist(circle)
        ab = AnnotationBbox(da, xy=(0,0), xycoords=("data", "data"), boxcoords=("data", "data"), box_alignment=(5.0,5.0), frameon=False)

        return ab

    def setData(self, nameList, dataList):
        self.nameList = nameList
        self.dataList = dataList

        # Open TopLevel component (graph holding all elements
        # in the platform)
        self.reportNewObject('TopLevel')

    def getAnotString(self, xCoord, YArray):
        returnString = ""
        
        returnString += "{:.4f}".format(np.interp(xCoord, elemX, elemY))+"\n"
        return returnString

    def updateLegend(self, mouseEvent):
            textSize = 15
            # Motion event where the tooltips and the graph component description
            # is presented

            xIndex = bisect.bisect_left(self.xArray, mouseEvent.xdata)

            cummYPos = 0
            pastYTop = 0

            pastAnnot = None
            legendText = ""
            for index, elem in enumerate(self.annot): 

                yval = np.interp(mouseEvent.xdata, self.xArray, self.localListToPlotY[index])
                cummYPos += yval

                                
                # If the marker is not inside the plot limits then do not render it    
                elem.set_visible(self.checkInsideDrawable(mouseEvent.xdata, cummYPos))
                    
                pastYBottom = max(pastYTop, cummYPos)
                pastYTop = pastYBottom
                elem.xytext = (mouseEvent.xdata, cummYPos)
                elem.xybox  = (mouseEvent.xdata, cummYPos)

                fullName = self.PartialNameList[index]
                componentName = fullName.split('/')[-1]
                legendText += "{:.4f} {}\n".format(yval, componentName)

                pastAnnot = elem

            self.legend.set_text(legendText)

            plotXLim = self.getPlotXLim()
            plotCoordSize = plotXLim[1] - plotXLim[0]

            self.legendArea.xybox = (mouseEvent.xdata+0.1*plotCoordSize, 0.1)
            self.legendArea.xytext = (mouseEvent.xdata+0.1*plotCoordSize, 0.1)
            self.legendArea.set_visible(True)
            self.canvas.draw_idle()

    def motionHandler(self, mouseEvent):
        #print "motion {0}, {1}".format(mouseEvent.xdata, mouseEvent.ydata)

        if self.startX:

            if mouseEvent.xdata and mouseEvent.ydata:
                self.zoomRectangle.set_width(mouseEvent.xdata - self.startX)
                self.zoomRectangle.set_height(mouseEvent.ydata - self.startY)

            self.canvas.draw_idle()

        elif self.annot and mouseEvent.xdata and  mouseEvent.ydata:
            self.updateLegend(mouseEvent)

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

        minX = self.zoomXlims[0]
        maxX = self.zoomXlims[1]
        minY = self.zoomYlims[0]
        maxY = self.zoomYlims[1]

        xlim = (max(currX- distXLow, minX), min(currX+distXHigh, maxX) )
        ylim = (max(currY- distYLow, minY), min(currY+distYHigh, maxY) )

        self.subPlot.set_xlim(xlim)
        self.subPlot.set_ylim(ylim)

        if self.annot and mouseEvent.xdata and  mouseEvent.ydata:
            self.updateLegend(mouseEvent)


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
        self.startX = []

    def pickHandler(self, mouseEvent):
        print "pick handler"

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
            self.buttonList.append(Checkbutton(self.subFrameCheckButtons, text=split(nameElem,"/")[-1],
                command=self.handleToggle, variable=self.checkerArray[nameElem], offvalue=0, onvalue=1,
                selectcolor="#"+R+G+B))
            
            self.buttonList[-1].toggle()

        indexR = 0
        indexC = 0
        for button in self.buttonList:
            button.grid(sticky = 'W', row = indexR, column = indexC)
            indexC += 1
            
            if( indexC>7):
                indexC = 0
                indexR += 1

        self.handleToggle()

    def handleToggle(self):
        enabledNames = []
        partialColorList = []
        index = 0
        for name, val in self.checkerArray.items():
            if val.get() == 1:
                enabledNames.append(name)
                partialColorList.append(self.colorList[index])
            index += 1

        self.enableData(enabledNames, partialColorList)

    def reportNewObject(self, name):

        subName = name.split('/')[-1]
        #self.subNameList = [subElem for subElem in self.nameList if name in subElem and name != subElem.split('/')[-1] ]
        self.subNameList = [subElem for subElem in self.nameList if subName == subElem.split('/')[-2] ]

        self.colorList = []
        nameListLen = len(self.subNameList)
        if nameListLen == 0:
            self.subNameList = [name]
            self.colorList = [(0.9,0.5,0.3)]
        else:
            self.colorList = [(1.0-x, (x*55)%1.0, (x*33) %1.0) for x in np.arange(0.1,1, 0.9/nameListLen)]
            #self.colorList = colorPallete
 
        self.updateToggleArray(self.subNameList, self.colorList)
        self.handleResize()

    def updateToggleArray(self, nameList, colorList):
        self.enableData(nameList, self.colorList)

