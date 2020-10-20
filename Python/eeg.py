

import time
import os
import sys
import platform
import struct
import operator
import math

# Import local package: (pywinusb 0.4.2)
sys.path.insert(0, './cyUSB')
import cyUSB as hid
#import pywinusb.hid as hid

# Import local package: (pycryptodome 4.2.6)
from Crypto.Cipher import AES
from Crypto import Random

DEVICE_POLL_INTERVAL = 0.001  # in seconds

tasks = [0]

class MyIO():
    
    def __init__(self):
        self.integerType = False
        self.noheader = False
        self.ovDelay = 100
        self.ovSamples = 4
        self.openvibe = False
        self.generic = False
        self.format = 0
        self.update_epoc = None
        self.newMask = None
        self.status = False
        self.setMask = []
        self.setMask = [None]*14
        self.recording = False
        self.recordInc = 1
        self.recordFile = "EEG_recording_"
        self.Delimiter = ", "
        self.samplingRate = 128
        self.channels = 40
        self.f = None
        
    def onData(self, uid, text):
        ioCommand = text.split(":::")
        return
    
    def onConnect(self, uid):
        self.status = True
        self.newMask = None
        if self.openvibe == True:
            return
        if self.noheader == True:
            return
        return
    
    def setOVSamples (self, samples):
        self.ovSamples = int(samples)
        print("OpenVibe Samples: " + str(samples))
        return
    
    def getOVSamples(self):
        return self.ovSamples
        
    def setInteger(self, state):
        self.integerType = state
        if state == True: 
            print("Data Type: Integer")
        else:
            print("Data Type: Float")
        return
    
    def getInteger(self):
        return self.integerType
        
    def setHeader(self, state):
        self.noheader = state
        if state == True:
            print("Header: Disabled")
        else:
            print("Header: Enabled")
        return
    
    def getHeader(self):
        return self.noheader
        
    def setGeneric(self, state):
        self.generic = state
        if state == True:
            print("Generic: Enabled")
        else:
            print("Generic: Disabled")
        return
    
    def getOVDelay(self):
        return int(self.ovDelay)
    
    def setOVDelay(self, delay):
        self.ovDelay = (int(delay) * 100)
        print("OpenVibe Delay: " + str(self.ovDelay))
        return

    def setOpenvibe(self, state):
        self.openvibe = state
        if state == True:
            print("OpenVibe: Enabled")
        if state == False:
            print("OpenVibe: Disabled")
        return        
        
    def getOpenvibe(self):
        return self.openvibe
    
    
    def onGeneric(self, uid):
        self.status = True
        self.generic = True
        if self.openvibe == True:
            return
        if self.noheader == True:
            return
        return
    
       
        
    def status(self):
        return self.status
    
    def onClose(self, uid):
        self.running = False
        return
    
    def modelChange(self):
        if 'newModel' not in globals():
            return 0
        aModel = self.newModel
        self.newModel = 0
        return self.aModel
     
    def update_epoc_settings(self, change):
        if change == 0:
            return self.update_epoc
        else:
            self.update_epoc = None
            return
    
    def startRecord(self, recordPacket):
        try:
            print>>self.f, recordPacket
            self.f.flush()
            os.fsync(self.f.fileno())
        except:
            pass

    def stopRecord(self):
        try:              
            if self.f == None:
                return
            self.f.flush()
            os.fsync(self.f.fileno())
            self.f.seek(0, os.SEEK_END)
            f_size = self.f.tell()
            #print("xxx:" + str(self.f.read(2))
            self.f.truncate((f_size -2))
            self.f.close()            # Remove last line.
            #
            #with open('./EEG-Logs/' + self.recordFile + '.csv', 'r+') as f:
            #    f.seek(0, os.SEEK_END) 
            #    while f.tell() and f.read(2) != '\r\n':
            #        f.seek(-4, os.SEEK_CUR)
            #    f.truncate()
            
        except Exception as msg:
            print("Error: " + str(msg))
                    
            pass
            
    def formatChange(self, newFormat):
        self.format = newFormat
        return
        
    def formatStatus(self):
        return self.format
        
    def isRecording(self):
        return self.recording
    
    def setSampling(self, rate):
        self.samplingRate = int(rate)
        return
    
    def getSampling(self):
        return self.samplingRate
        
    def setChannels(self, total):
        self.channels = int(total)
        return
    
    def getChannels(self):
        return self.channels
    
    def setKeyModel(self, key):
        self.KeyModel = key
        return
    
    def getKeyModel(self):
        return self.KeyModel

    def setDelimiter(self, string):
        self.Delimiter = str(string)
        return
    
    def isGeneric(self):
        return self.generic
        
    def getDelimiter(self):
        return str(self.Delimiter)
    
    def maskChange(self):
        return self.newMask
    
    def getMask(self, select):
        self.newMask = None
        return self.setMask[int(select)]
    
    def setReport(self, report):
        self.report = report
        self.epoc_plus_usb = True
    
    def setInfo(self, info, infoData):
        if info == "Device":
            self.infoDevice = str(infoData)
        if info == "Serial":
            self.infoSerial = str(infoData)
        return
        

        
class EEG(object):
    
    def __init__(self, model, io, config):
        global myIOinstance
        config = config.lower()
        self.time_delay = .001
        self.KeyModel = model
        self.eeg_devices = []
        self.counter = "0"
        self.serial_number = ""
        self.hid = None
        self.myIOinstance = io
        self.myKey = self.Setup(model, config)
        self.recordInc = 1
        self.samplingRate = 128
        self.epoc_plus_usb = False
        self.report = None
        self.Delimiter = ", "
        self.channels = 40
        self.blankCSV = False
        self.generic = False
        self.openvibe = False
        self.integerType = False
        
        self.mask = {}
        self.mask[0] = [10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7]
        self.mask[1] = [28, 29, 30, 31, 16, 17, 18, 19, 20, 21, 22, 23, 8, 9]
        self.mask[2] = [46, 47, 32, 33, 34, 35, 36, 37, 38, 39, 24, 25, 26, 27]
        self.mask[3] = [48, 49, 50, 51, 52, 53, 54, 55, 40, 41, 42, 43, 44, 45]
        self.mask[4] = [66, 67, 68, 69, 70, 71, 56, 57, 58, 59, 60, 61, 62, 63]
        self.mask[5] = [84, 85, 86, 87, 72, 73, 74, 75, 76, 77, 78, 79, 64, 65]
        self.mask[6] = [102, 103, 88, 89, 90, 91, 92, 93, 94, 95, 80, 81, 82, 83]
        self.mask[7] = [140, 141, 142, 143, 128, 129, 130, 131, 132, 133, 134, 135, 120, 121]
        self.mask[8] = [158, 159, 144, 145, 146, 147, 148, 149, 150, 151, 136, 137, 138, 139]
        self.mask[9] = [160, 161, 162, 163, 164, 165, 166, 167, 152, 153, 154, 155, 156, 157]
        self.mask[10] = [178, 179, 180, 181, 182, 183, 168, 169, 170, 171, 172, 173, 174, 175]
        self.mask[11] = [196, 197, 198, 199, 184, 185, 186, 187, 188, 189, 190, 191, 176, 177]
        self.mask[12] = [214, 215, 200, 201, 202, 203, 204, 205, 206, 207, 192, 193, 194, 195]
        self.mask[13] = [216, 217, 218, 219, 220, 221, 222, 223, 208, 209, 210, 211, 212, 213]
        
        if "blankdata" in config:     self.blank_data = True
        else:                         self.blank_data = False
        
        if "blankcsv" in config:      self.blankCSV = True
        else:                         self.blankCSV = False
        
        if "nocounter" in config:     self.no_counter = True
        else:                         self.no_counter = False
                    
        if "nobattery" in config:     self.nobattery = True
        else:                         self.nobattery = False
                            
        if "baseline" in config:      self.baseline = True
        else:                         self.baseline = False
        
        if "noheader" in config:      self.noheader = True
        else:                         self.noheader = False
                        
        if "integer" in config:       self.integerType = True
        else:                         self.integerType = False
                
        if "outputdata" in config:    self.outputData = True
        else:                         self.outputData = False
        
        if "generic" in config:       self.generic = True
        else:                         self.generic = False
        
        if "openvibe" in config:      self.openvibe = True
        else:                         self.openvibe = False
        
        if "outputencrypt" in config: self.outputEncrypt = True
        else:                         self.outputEncrypt = False
        
            

        
        
        self.format = 0
            
        self.myIOinstance.setInteger(self.integerType)
        self.myIOinstance.formatChange(self.format)
        self.myIOinstance.setHeader(self.noheader)
        self.myIOinstance.setGeneric(self.generic)
        self.myIOinstance.setOpenvibe(self.openvibe)


    
    def Setup(self, model, config):
        # 'EPOC BCI', 'Brain Waves', 'Brain Computer Interface USB Receiver/Dongle', 'Receiver Dongle L01'
        deviceList = ['EPOC+','EEG Signals', '00000000000', 'Emotiv RAW DATA']
        devicesUsed = 0

                
        for device in hid.find_all_hid_devices():
            if "info" in config:
                print("Product name " + device.product_name)
                print("device path " + device.device_path)
                print("instance id " + device.instance_id)
                print("_" * 80 + "\r\n")
            useDevice = ""
            for i, findDevice in enumerate(deviceList):
                
                if device.product_name == deviceList[i]:
                    print("\r\n>>> Found EEG Device >>> " +  findDevice + "\r\n")
                    devicesUsed += 1
                    self.hid = device
                    self.hid.open()
                    self.serial_number = device.serial_number
                    device.set_raw_data_handler(self.dataHandler)
                    print("> Using Device: " + device.product_name + "\r\n")
                    print("  Serial Number: " + device.serial_number + "\r\n\r\n")
                    if device.product_name == 'EPOC+':
                        deviceList[1] = 'empty'
                            
        if devicesUsed == 0 or i == 0:
            print("\r\n> No Device Selected. Exiting . . .")
            os._exit(0)
        
        self.myIOinstance.setInfo("Device", device.product_name)
        self.myIOinstance.setInfo("Serial", device.serial_number)
            
        sn = self.serial_number
        
        k = ['\0'] * 16


        k = [sn[-1],sn[-2],sn[-2],sn[-3],sn[-3],sn[-3],sn[-2],sn[-4],sn[-1],sn[-4],sn[-2],sn[-2],sn[-4],sn[-4],sn[-2],sn[-1]]
        self.samplingRate = 256
        self.channels = 40
            
        self.myIOinstance.setSampling(self.samplingRate)
        self.myIOinstance.setChannels(self.channels)
        self.myIOinstance.setKeyModel(model)
        
        key = ''.join(k)
        print("key = " + str(key))
        return str(key)
            

    def dataHandler(self, data):
        tasks[0] = (''.join(map(chr, data[1:])))
        return True

    
    def convertEPOC_PLUS(self, value_1, value_2):
        
        edk_value = "%.8f" % (((int(value_1) * .128205128205129) + 4201.02564096001) + ((int(value_2) -128) * 32.82051289))
        if self.integerType == True:
            return str(int(float(edk_value)))
        return edk_value
       
    def get_data(self):

        key = self.myKey
        myio = self.myIOinstance  

        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
        
        self.Delimiter = str(self.myIOinstance.getDelimiter())
        

        self.generic = self.myIOinstance.isGeneric()
    

        

        if True:
           if True:
                
                check_mask = self.myIOinstance.maskChange()
                
                self.format = self.myIOinstance.formatStatus()
                
                if check_mask != None:
                    self.mask[check_mask] = self.myIOinstance.getMask(check_mask)
                    print(self.mask[check_mask])
                
                n = 1
                while(len(tasks) == 0):
                    n = 3#dummy instr
                
                task = tasks[0].encode("latin-1") # 1 carater to 1 byte
                try:
                    data = cipher.decrypt(task[:16]) + cipher.decrypt(task[16:])
                    packet_data = ""
                                        

                    
                    if self.KeyModel == 6 or self.KeyModel == 5:
                        if self.no_counter == True:
                            packet_data = ""
                        else:
                            packet_data = str((data[0])) + self.Delimiter + str((data[1])) + self.Delimiter
                                
                        # Format 0: Default.  
                        if self.format < 1:
                            for i in range(2,16,2):
                                packet_data = packet_data + str(self.convertEPOC_PLUS(str((data[i])), str((data[i+1])))) + self.Delimiter

                              
                            for i in range(18,len(data),2):
                                packet_data = packet_data + str(self.convertEPOC_PLUS(str((data[i])), str((data[i+1])))) + self.Delimiter
                                   
                            
                            packet_data = packet_data  + str((data[16])) + str(self.Delimiter) + str((data[17])) 
                   
                            return [float(i) for i in packet_data.split(self.Delimiter)] 

                except Exception as exception2:
                    print(str(exception2))
        
    