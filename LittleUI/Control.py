import os
import sys,os
import math
import fileinput
import binascii
from os import walk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import thread


L = sys.path
L.append(os.getcwd()) # need to add current working directory
# to python path to import defined functions
import time
from time import sleep
import serial
import serial.tools.list_ports

import io
import string
import array
import re
import binascii
import struct



class GOEControlClass:
    timer = 100
    SensorSerial = None
    command_one = '010306000002C483'
    command_two = '0103061400028487'
    command_three = '010306280002448B'
    command_four = '010306780002449A'
    command_all = '01039C480008EA4A'
    command_cleanAll = '01100652000204000000059CE9'
    StopSymbol = 0

    def GetSensorValue(self,command):
        if(self.SensorSerial.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            StrValue = binascii.unhexlify(command)
            SendCommand = self.SensorSerial.write(StrValue)
            ReceiveValue = self.SensorSerial.read(9)
            ReceiveValue = binascii.hexlify(ReceiveValue)
            GetReceiveValue = ReceiveValue[6:14]
            # return str(GetReceiveValue)
            err = int(GetReceiveValue,16)
            if (err>2147483648):
                err = long(err) 
                err = err ^ 4294967295
                err = err + 1
                temp = "-"+str(err)
                return temp
            else:
                return str(err)
        except:
            self.strErrorMessage = "GetSensorValue fail"
            return -1

    def GetAllLines(self,command):
        if(self.SensorSerial.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            StrValue = binascii.unhexlify(command)
            SendCommand = self.SensorSerial.write(StrValue)
            ReceiveValue = self.SensorSerial.read(21)
            ReceiveValue = binascii.hexlify(ReceiveValue)

            GetReceiveValue_1 = ReceiveValue[6:14]
            GetReceiveValue_1 = int(GetReceiveValue_1,16)

            GetReceiveValue_2 = ReceiveValue[14:22]
            GetReceiveValue_2 = int(GetReceiveValue_2,16)

            GetReceiveValue_3 = ReceiveValue[22:30]
            GetReceiveValue_3 = int(GetReceiveValue_3,16)

            GetReceiveValue_4 = ReceiveValue[30:38]
            GetReceiveValue_4 = int(GetReceiveValue_4,16)
            # return ReceiveValue
            list_one = []
            list_one = [GetReceiveValue_1 , GetReceiveValue_2 , GetReceiveValue_3 , GetReceiveValue_4]
            for i in range(0,4,1):
                if(list_one[i]>2147483648):
                    list_one[i] = long(list_one[i])
                    list_one[i] = list_one[i] ^ 4294967295
                    list_one[i] = list_one[i] + 1
                    list_one[i] = -list_one[i]
                else:
                    list_one[i] = list_one[i]
            return list_one
        except:
            self.strErrorMessage = "GetAllLines fail"
            return -1

    def CleanAllLines(self,command):
        if(self.SensorSerial.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            StrValue = binascii.unhexlify(command)
            self.SensorSerial.write(StrValue)
            if(self.SensorSerial.isOpen()):
                self.SensorSerial.close()
            return 0

        except:
            self.strErrorMessage = "CleanAllLines fail"
            return -1

    #ChooseCOM function
    def ChooseCOM(self,serialName):
        try:
            self.SensorSerial = serial.Serial(port=serialName, baudrate=19200, bytesize=8, parity='N', stopbits=2, timeout=None, xonxoff=0, rtscts=0)
            if(self.SensorSerial.isOpen()):
                #command = [0x01,0x03,0x9C,0x48,0x00,0x02,0x6A,0x4D]
                # command = '01039C4800026A4D'   #int firsLine
                # #command = '010306000002C483'  #float firstLine
                # #command = '0103061400028487'  #float secondLine
                # #command = '010306280002448B'  #float thirdLine
                # #command = '010306780002449A'  #float fourthLine
                # #command = '01039C480004EA4F'  #1-2Lines
                # #command = '01039C4800066B8E'  #1-3Lines
                # #command = '01039C480008EA4A'  #1-4Lines
                return 0
            else:
                return 1
        except:
            self.strErrorMessage =  "ChooseCOM fail"
            return -1

    # Open Serial
    def OpenSerial(self):
        try:
            port_list = list(serial.tools.list_ports.comports())
            if(len(port_list) < 0):
                self.strErrorMessage = "fail:There is no serial port"
                return -1
            bFindSerialPort = False
            #for i in range(0, len(port_list)):
            err = self.ChooseCOM("COM7")
            # for i in range(0,1):
            #     err =  self.ChooseCOM("/dev/ttyS1")
            if(err == 0):
                bFindSerialPort = True
                return 0
                #self.ser.stop_bits = 1
                #self.ser.flow_control = 'None'
            if(bFindSerialPort == False):
                self.strErrorMessage = "There is no report"
                return -1
        except:
            self.strErrorMessage =  "Open serial port fail"
            return -1
        return 0

    # Close Serial
    def CloseSerial(self):
        try:
            if(self.SensorSerial.isOpen):
                self.SensorSerial.close()
            return 0
        except:
            self.strErrorMessage =   "CloseSerial fail"
            return -1