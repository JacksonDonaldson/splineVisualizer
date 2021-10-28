import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import tkinter as tk
import time

def findSpline(x1,y1,v1,x2,y2,v2, curviness = 1):
    steps = 25
    points = []
    
    xpoints = []
    ypoints = []
    for i in range(steps+1):
        t= i/steps
        t2 = t * t
        t3 = t*t*t

        p0 = (x1,y1)

        p1 = (x2,y2)

        h00 = 2*t3 - 3*t2 + 1
        h10 = t3-2*t2 + t
        h01 = -2 * t3 + 3 * t2
        h11 = t3 - t2
        
        px = h00*p0[0] + curviness*h10*v1[0] + h01*p1[0] + curviness*h11*v2[0]
        py = h00*p0[1] + curviness*h10*v1[1] + h01*p1[1] + curviness*h11*v2[1]
        xpoints.append(px)
        ypoints.append(py)
    return [xpoints,ypoints]


def updateSplineGraph(foo):
    print('updating')
    print(foo)
    time.sleep(.1)
    plt.clf()
    global splinePoints, fieldMarkers
    if len(splinePoints) < 2:
        return True

    #add in all the splines
    for i in range(len(splinePoints)-1):
        p1 = splinePoints[i]
        p2 = splinePoints[i+1]
        try:
            print(1)
            x1 = float(p1[0].get())
            print(2)
            y1=float(p1[1].get())
            print(3)
            v1 = (float(p1[2].get()),float(p1[3].get()))
            print(4)
            curve=float(p1[4].get())

            print(5)
            x2 = float(p2[0].get())
            print(6)
            y2=float(p2[1].get())
            print(7)
            v2 = (float(p2[2].get()),float(p2[3].get()))

        except:
            print("Invalid value found")
            continue
        line = findSpline(x1,y1,v1,x2,y2,v2,curve)
        plt.plot(line[0],line[1])

    #add in field markers
    for marker in fieldMarkers:
        try:
            x = float(marker[0].get())
            y=float(marker[1].get())
            r=float(marker[2].get())

            circ = plt.Circle((x,y),r)
            plt.gca().add_patch(circ)
        except:
            print("invalid fieldmarker")
        
    #do all the rescaling stuff
    plt.gca().relim()

    try:
        xSMi=float(xScaleMin.get())
        xSMa=float(xScaleMax.get())
        ySMi=float(yScaleMin.get())
        ySMa=float(yScaleMax.get())
        plt.xticks([(xSMa-xSMi)*(i/10) + xSMi for i in range(11)])
        plt.yticks([(ySMa-ySMi)*(i/10) + ySMi for i in range(11)])
    except:
        print("failed scale")
        plt.gca().autoscale_view()

        
    plt.show()
    return True

def createLabel(text,row,column,columnspan=1):
    global win
    label = tk.Label(win,text=text)
    label.grid(column=column,row=row,columnspan=columnspan)
    return label

def createEntry(row,column,columnspan=1):
    global win
    entry = tk.Entry(win,width=10)#,validate="key",validatecommand=updateSplineGraph)
    entry.bind("<Return>",updateSplineGraph)
    entry.grid(column=column,row=row)
    return entry


def createNextSplinePoint():
    global splinePoints
    pNum=len(splinePoints)
    r=pNum+4

    createLabel("Point " + str(pNum) + ":",r,0)
    createLabel("x:", r,1)
    createLabel("y:",r,3)
    createLabel("dx/dt:",r,5)
    createLabel("dy/dt:",r,7)
    createLabel("curve:",r,9)
    
    x = createEntry(r,2)
    y = createEntry(r,4)
    dx = createEntry(r,6)
    dy = createEntry(r,8)
    curve = createEntry(r,10)
    
    splinePoints.append([x,y,dx,dy,curve])

def createNextMarker():
    global fieldMarkers
    fNum = len(fieldMarkers)
    r = fNum+101
    createLabel("Marker " + str(fNum) + ":",r,0)
    createLabel("x:",r,1)
    createLabel("y:",r,3)
    createLabel("r:",r,5)

    x = createEntry(r,2)
    y=createEntry(r,4)
    r=createEntry(r,6)

    fieldMarkers.append([x,y,r])
    
def createWindow(foo):
    global win, splinePoints, xScaleMin,yScaleMin,xScaleMax,yScaleMax, fieldMarkers
    splinePoints=[]
    fieldMarkers=[]
    win = tk.Tk(className="Line Input")
    
    createLabel("Scale Values: (leave blank for autoscale)",0,0,4)
    createLabel("xMin:",1,0)
    createLabel("yMin:",2,0)
    createLabel("xMax:",1,2)
    createLabel("yMax:",2,2)

    xScaleMin = createEntry(1,1)
    yScaleMin = createEntry(2,1)
    xScaleMax = createEntry(1,3)
    yScaleMax = createEntry(2,3)
    
    createLabel("Spline Points: (Enter to update)",3,0,10)
    createNextSplinePoint()
    createNextSplinePoint()
    
    button = tk.Button(win,text="Add new point",command=createNextSplinePoint)

    button.grid(column=0,row=99)

    createLabel("Field Position Markers:",100,0,10)
    createNextMarker()
    
    button2=tk.Button(win,text="Add Field Position Marker", command = createNextMarker)
    button2.grid(column=0,row=200)

    
    return win
        

    #win.mainloop()

#1: open matplot, with plot and button to open line creation window
#on button click: launch tkinter, with options to create new point, ect
#graph as we go
def main():
    global main_ax
    button_ax = plt.axes([0.1, 0.05, 0.8, 0.05])
    main_ax = plt.axes([0.1, 0.2, 0.8, 0.65])
    startButton = plt.Button(button_ax,"Create New Line")
    startButton.on_clicked(createWindow)
    plt.show()

main()
