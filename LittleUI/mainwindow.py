from Tkinter import *
import ttk
import os
import tkFont
import tkMessageBox
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
from Control import *
import threading

goectl = GOEControlClass ()

root = Tk ()
var_com = StringVar ()


def ButtonState(state):
    if (state):
        buttonClose.configure ( state='active' )  # close serial port
        buttonGetFirstLine.configure ( state='active' )
        buttonGetSecondLine.configure ( state='active' )
        buttonGetThirdLine.configure ( state='active' )
        buttonGetFourthLine.configure ( state='active' )
        buttonGetAllLines.configure ( state='active' )
        buttonCleanAllLines.configure ( state='active' )
        buttonPainting.configure ( state='active' )
        buttonStopPainting.configure ( state='active' )
    else:
        buttonClose.configure ( state='disabled' )  # close serial port
        buttonGetFirstLine.configure ( state='disabled' )
        buttonGetSecondLine.configure ( state='disabled' )
        buttonGetThirdLine.configure ( state='disabled' )
        buttonGetFourthLine.configure ( state='disabled' )
        buttonGetAllLines.configure ( state='disabled' )
        buttonCleanAllLines.configure ( state='disabled' )
        buttonPainting.configure ( state='disabled' )
        buttonStopPainting.configure ( state='disable' )


# open port
def actionOPenPort():
    try:
        err = goectl.OpenSerial ()
        if (err == -1):
            tkMessageBox.showinfo ( "Error", "actionOPenPort fail" )
            return
        ButtonState ( True )
        buttonOpenPort.configure ( state='disabled' )
    except:
        tkMessageBox.showinfo ( "Error", "actionOPenPort fail" )


# close port
def actionClose():
    print 'actionClose'
    try:
        err = goectl.CloseSerial ()
        if (err != 0):
            tkMessageBox.showinfo ( "Error", "error")
        ButtonState ( False )
        buttonOpenPort.configure ( state='active' )
    except:
        tkMessageBox.showinfo ( "Error", "Close serial port fail" )


#getfirstline
def actionGetFirstLine():
    print 'actionGetFirstLine'
    err = goectl.GetSensorValue ( goectl.command_one )
    varGetFirstLine.set ( str ( err ) )


#getsecondline
def actionGetSecondLine():
    print 'actionGetSecondLine'
    err = goectl.GetSensorValue ( goectl.command_two )
    varGetSecondLine.set ( str ( err ) )


#getthirdline
def actionGetThirdLine():
    print 'actionGetThirdLine'
    err = goectl.GetSensorValue ( goectl.command_three )
    varGetThirdLine.set ( str ( err ) )


#getfourthline
def actionGetFourthLine():
    print 'actionGetFourthLine'
    err = goectl.GetSensorValue ( goectl.command_four )
    varGetFourthLine.set ( str ( err ) )


#getAllLines
def actionGetAllLines():
    err = goectl.GetAllLines ( goectl.command_all )
    print err[0]
    print err[1]
    print err[2]
    print err[3]

    varGetFirstLine.set ( err[0] )
    varGetSecondLine.set ( err[1] )
    varGetThirdLine.set ( err[2] )
    varGetFourthLine.set ( err[3] )
    varGetAllLines.set ( err[0] + err[1] + err[2] + err[3] )


#claen
def actionCleanAllLines():
    try:
        err = goectl.CleanAllLines ( goectl.command_cleanAll )
        if (err != 0):
            tkMessageBox.showinfo ( "Error", "CleanAllLines error" )
        varGetFirstLine.set ( '' )
        varGetSecondLine.set ( '' )
        varGetThirdLine.set ( '' )
        varGetFourthLine.set ( '' )
        varGetAllLines.set ( '' )
        ButtonState ( False )
        buttonOpenPort.configure ( state='active' )
        buttonStopPainting.configure ( state='disable' )
    except:
        tkMessageBox.showinfo ( "Error", "CleanAllLines fail" )
        return -1


# painting

def actionStartPainting():
    ax = []
    ay1 = []
    ay2 = []
    ay3 = []
    ay4 = []
    t = 0.0
    try:
        for i in xrange ( 0, 51, 1 ):
            start = time.time ()
            ax.append ( t )
            ay = goectl.GetAllLines ( goectl.command_all )
            ay[0] = float ( ay[0] )
            ay[0] = ay[0] / 100

            ay[1] = float ( ay[1] )
            ay[1] = ay[1] / 100

            ay[2] = float ( ay[2] )
            ay[2] = ay[2] / 100

            ay[3] = float ( ay[3] )
            ay[3] = ay[3] / 100
            # ay1.append(0)
            # ay2.append(1)
            # ay3.append(2)
            # ay4.append(3)
            ay1.append ( ay[0] )
            ay2.append ( ay[1] )
            ay3.append ( ay[2] )
            ay4.append ( ay[3] )
            plt.ylabel ( "(Units/N)" )
            plt.xlabel ( "(Displacement/mm)" )
            plt.xticks ( [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0] )
            plt.plot ( ax, ay1, 'b' )
            plt.plot ( ax, ay2, 'k' )
            plt.plot ( ax, ay3, 'r' )
            plt.plot ( ax, ay4, 'c' )
            plt.legend ( ('firstline', 'secondline', 'thirdline', 'fourthline'), bbox_to_anchor=(1.0, 1), loc=2,
                         shadow=True )
            plt.pause ( 0.01 )
            t = t + 0.1
            end = time.time ()
            print end - start
            # plt.ioff()
            if (goectl.StopSymbol == 0):
                continue
            else:
                plt.savefig ( "Painting.png" )
                break
            # plt.cla()
            # plt.clf()
            # plt.close()
            # if(goectl.StopSymbol != 0):
            # 	return
            # actionStartPainting()
            # plt.show()
    except:
        tkMessageBox.showinfo ( "Error", "Painting fail" )
        return -1


# stop painting

def actionStopPainting():
    try:
        goectl.StopSymbol = 1
        buttonPainting.configure ( state='disable' )
    except:
        tkMessageBox.showinfo ( "Error", "actionStopPainting fail" )
        return -1


# set title
root.title ( 'Demo V1.0' )
helv10 = tkFont.Font ( family="Helvetica", size=12, weight="bold" )

# com port selection
Label ( root, text='COM', width=12 ).grid ( row=0, column=1 )
buttonOpenPort = Button ( root, text='OpenPort', command=actionOPenPort, width=12 )
buttonOpenPort.grid ( row=0, column=2 )

# close
buttonClose = Button ( root, text='Close', command=actionClose, width=12 )
buttonClose.grid ( row=0, column=3 )
buttonClose.configure ( state='disabled' )

# get firstLine
buttonGetFirstLine = Button ( root, text='GetFirstLine', command=actionGetFirstLine, width=12 )
buttonGetFirstLine.grid ( row=1, column=1 )
buttonGetFirstLine.configure ( state='disabled' )
varGetFirstLine = StringVar ()
GetFirstLine = Entry ( root, textvariable=varGetFirstLine, width=12 )
GetFirstLine.grid ( row=1, column=2 )

# get secondLine
buttonGetSecondLine = Button ( root, text='GetSecondLine', command=actionGetSecondLine, width=12 )
buttonGetSecondLine.grid ( row=2, column=1 )
buttonGetSecondLine.configure ( state='disabled' )
varGetSecondLine = StringVar ()
GetSecondLine = Entry ( root, textvariable=varGetSecondLine, width=12 )
GetSecondLine.grid ( row=2, column=2 )

# get thirdLine
buttonGetThirdLine = Button ( root, text='GetThirdLine', command=actionGetThirdLine, width=12 )
buttonGetThirdLine.grid ( row=3, column=1 )
buttonGetThirdLine.configure ( state='disabled' )
varGetThirdLine = StringVar ()
GetThirdLine = Entry ( root, textvariable=varGetThirdLine, width=12 )
GetThirdLine.grid ( row=3, column=2 )

# get fourthLine
buttonGetFourthLine = Button ( root, text='GetFourthLine', command=actionGetFourthLine, width=12 )
buttonGetFourthLine.grid ( row=4, column=1 )
buttonGetFourthLine.configure ( state='disabled' )
varGetFourthLine = StringVar ()
GetFourthLine = Entry ( root, textvariable=varGetFourthLine, width=12 )
GetFourthLine.grid ( row=4, column=2 )

# get allLines
buttonGetAllLines = Button ( root, text='GetAllLines', command=actionGetAllLines, width=12 )
buttonGetAllLines.grid ( row=5, column=1 )
buttonGetAllLines.configure ( state='disabled' )
varGetAllLines = StringVar ()
GetAllLines = Entry ( root, textvariable=varGetAllLines, width=12 )
GetAllLines.grid ( row=5, column=2 )

# cleanAllLines
buttonCleanAllLines = Button ( root, text='CleanAllLines', command=actionCleanAllLines, width=12 )
buttonCleanAllLines.grid ( row=3, column=3 )
buttonCleanAllLines.configure ( state='disabled' )

# start Painting
buttonPainting = Button ( root, text='StartPainting', command=actionStartPainting, width=12 )
buttonPainting.grid ( row=3, column=4 )
buttonPainting.configure ( state='disabled' )

# stop Painting
buttonStopPainting = Button ( root, text='StopPainting', command=actionStopPainting, width=12 )
buttonStopPainting.grid ( row=4, column=4 )
buttonStopPainting.configure ( state='disabled' )

root.mainloop ()