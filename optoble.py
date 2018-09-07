"""
OptoBLE Controller: Bluetooth Low Energy conroller for optogenetic stimulator implants

    @author: Ian Baumgart ibaumgart@wisc.edu//ianbaumgart96@gmail.com
    @version: 1.7

    TODO:
        Create connection signal to monitor continued connection to device

        Implement interrupts for the temperature monitor and connection signal

        Update UI for aesthetics and sizing
        
"""
import binascii
import struct
import time
import tkFont
import random
from Tkinter import *
from bluepy.btle import Scanner, DefaultDelegate, Peripheral

DBG = True

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

    def handleNotification(self, cHandle, data):
        print("note received")
        print(data)


class optoGUI:
    def __init__(self, master):
        self.master = master
        master.title = "optoBLE"
        self.isConnected = False
        self.sending = False
        global DBG
        global fSz
        global scrWidth
        global scrHeight
        global xOffset
        
        self.label = Label(master, text="BLE Optogenetic Stimulator", font=thisFont)
        self.label.grid(row=0, column=0, columnspan=2, padx=xOffset)

        self.search_button = Button(master, text="Search", command=self.rfdScan, activebackground="green", font=thisFont)
        self.search_button.grid(row=1, column=0, padx=xOffset)

        self.connect_button = Button(master, text="Connect", command=self.rfdConnect, activebackground="green", font=thisFont)
        self.connect_button.grid(row=2, column=0, padx=xOffset)

        self.disconnect_button = Button(master, text="Disconnect", command=self.rfdDisconnect, activebackground="red", font=thisFont)
        self.disconnect_button.grid(row=3, column=0, padx=xOffset)
        #self.disconnect_button.bind("<Button-1>", master.quit)

        self.devLb = Listbox(master, height=6, font=thisFont)
        self.devLb.grid(row=1,column=1,columnspan=1,rowspan=3, padx=xOffset)

        self.t1On_label = Label(master, text="Blue Time On", font=thisFont)
        self.t1On_label.grid(row=4, column=0, padx=xOffset)
        self.t1On_entry = Entry(master, font=thisFont)
        self.t1On_entry.grid(row=4, column=1, padx=xOffset)
        self.ms1label = Label(master, text="ms", font=thisFont)
        self.ms1label.grid(row=4, column=2)
        
        self.t1Off_label = Label(master, text="Blue Time Off", font=thisFont)
        self.t1Off_label.grid(row=5, column=0, padx=xOffset)
        self.t1Off_entry = Entry(master, font=thisFont)
        self.t1Off_entry.grid(row=5, column=1, padx=xOffset)
        self.s1label = Label(master, text="s", font=thisFont)
        self.s1label.grid(row=5, column=2)
        
        self.t2On_label = Label(master, text="Red Time On", font=thisFont)
        self.t2On_label.grid(row=6, column=0, padx=xOffset)
        self.t2On_entry = Entry(master, font=thisFont)
        self.t2On_entry.grid(row=6, column=1, padx=xOffset)
        self.ms2label = Label(master, text="ms", font=thisFont)
        self.ms2label.grid(row=6, column=2)
        
        self.t2Off_label = Label(master, text="Red Time Off", font=thisFont)
        self.t2Off_label.grid(row=7, column=0, padx=xOffset)
        self.t2Off_entry = Entry(master, font=thisFont)
        self.t2Off_entry.grid(row=7, column=1, padx=xOffset)
        self.s2label = Label(master, text="s", font=thisFont)
        self.s2label.grid(row=7, column=2)
        
        self.cyc_label = Label(master, text="Number of Cycles", font=thisFont)
        self.cyc_label.grid(row=8, column=0, padx=xOffset)
        self.cyc_entry = Entry(master, font=thisFont)
        self.cyc_entry.grid(row=8, column=1, padx=xOffset)
        
        self.send_button = Button(master, text="Send", command=self.rfdSend, font=thisFont)
        self.send_button.grid(row=9, column=1, padx=xOffset)

        self.temp_label = Label(master, text="", font=thisFont)
        self.temp_label.grid(row=9, column=0, padx=xOffset)

        self.rssi_label = Label(master, text="RSSI", font=thisFont)
        self.rssi_label.grid(row=0, column=2)
        self.rssiLb = Listbox(master, height=6, width=3, font=thisFont)
        self.rssiLb.grid(row=1,column=2,columnspan=1,rowspan=3)

        self.cnt_label = Label(master, text="C", font=thisFont)
        self.cnt_label.grid(row=0, column=3)
        self.cntLb = Listbox(master, height=6, width=3, font=thisFont)
        self.cntLb.grid(row=1,column=3,columnspan=1,rowspan=3)

        self.defaultbg = root.cget('bg')

        self.connected_label = Label(master, text="Connected", font=thisFont)

        #self.disconnect_button.bind("<Button-1>", master.quit)


    def rfdScan(self):
        scanner = Scanner()
        devices = scanner.scan(15.0)

        self.devLb.delete(0,self.devLb.size()-1)
        self.devlist = []
        self.rssiLb.delete(0,self.rssiLb.size()-1)
        self.cntLb.delete(0,self.rssiLb.size()-1)
        if(DBG):
            self.devLb.insert(END,"TEST_DEVICE")
            self.rssiLb.insert(END,0)
        for dev in devices:
            print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
    #        print "Temp %s" % (dev.
    #       print(dev.getValueText(9)[0:7])
    #       print(dev.addrType)
            if(dev.getValueText(9) != None):
                #print("  None check passed")
                if(dev.getValueText(9)[0:7]=="optoRFD"):
                    print " RFDuino device found"
                    for (adtype, desc, value) in dev.getScanData():
                        print "  %s = %s" % (desc, value)
                    self.devLb.insert(END,dev.getValueText(9))
                    self.devlist.append(dev.addr)
                    self.rssiLb.insert(END,dev.rssi)
                    self.cntLb.insert(END,"")
    
                    
    def rfdReceive(self):
        #print "rfd"
        if(self.isConnected==True):
            try:
                print "receiving from " + self.p.addr
                tval = 0
                recService = self.p.getServiceByUUID(cUUID)
                recChar = recService.getCharacteristics()[0]
                if (recChar.supportsRead()):
                    try:
                        tval = binascii.b2a_hex(recChar.read())
                        tval = binascii.unhexlify(tval)
                        tval = struct.unpack('f', tval)[0]
                        tstr = "%.2f deg C" % tval
                        if(tstr == "1.00 deg C"):
                            print str(tval)
                            print "complete"
                            self.temp_label.configure(text="complete")
                            #time.sleep(1)
                            #self.rfdDisconnect()
                        else:
                            if(tstr == "0.00 deg C"):
                                print str(tval)
                                print "incomplete"
                                self.temp_label.configure(text="incomplete")
                                time.sleep(1)
                                self.rfdDisconnect()
                            else:
                                print str(tval) + " deg C"
                                self.temp_label.configure(text="%.2f deg C" % tval)
                    except:
                        print "no data"
                        self.temp_label.configure(text="no temp")
            except:
                if(DBG):
                    tval = random.randint(27,40)
                    self.temp_label.configure(text="%.2f deg C" % tval)
                else:
                    print("  disconnected, please reconnect")
                    self.connect_button.configure(fg = "black")
                    self.cntLb.delete(0,10)
                    self.isConnected = False
                    self.rfdConnect

        root.after(5000, self.rfdReceive)

        
    def rfdConnect(self):
        print ""
        if(DBG):
            self.isConnected = True
            self.connect_button.configure(fg = "green")
            self.cntLb.delete(0)
            self.cntLb.insert(0,"X")
        while (self.isConnected==False):      
            cInd = self.devLb.curselection()
            cDevice = self.devlist[cInd[0]]
            print "connecting to " + cDevice
            try:
                self.p = Peripheral(cDevice,"random")
                self.p.setDelegate(ScanDelegate)
                self.isConnected = True
                self.cntLb.delete(cInd[0])
                self.cntLb.insert(cInd[0],"X")
                self.connect_button.configure(fg = "green")
                print "connected"
                time.sleep(1)
            except:
                print(" retrying connection")
                time.sleep(2)
        """
        services=self.p.getServices()
        print("Services found:")
        for service in services:
            print(service)
            for char in service.getCharacteristics():
                print char
                print char.supportsRead()
        """

    def rfdSend(self):

        outStr = 'rats!'+self.cyc_entry.get()+'!'+self.t1On_entry.get()+'!'+self.t1Off_entry.get()+'!'+self.t2On_entry.get()+'!'+self.t2Off_entry.get()
        
        try:
            sendService = self.p.getServiceByUUID(cUUID)
        #    print("in service: " + str(sendService))
            sendChar = sendService.getCharacteristics()[1]
            print(sendChar)
            print(" send attempted")
            print("  " + outStr)
            #ch.write(struct.pack('<B', 0x01));
            sendChar.write(outStr)
            self.isSending = True
            #self.rfdDisconnect
            """
            self.send_button.configure(bg="green")
            time.sleep(0.5)
            self.send_button.configure(bg=self.defaultbg)
            self.isConnected = False
            self.connect_button.configure(fg = "black")
            """
            #self.temp_label.configure(text="Running")
            #time.sleep(time_tot)
        except:
            if(DBG):
                self.isSending = True
                self.temp_label.configure(text="Running")
                time.sleep(time_tot)
            else:
                print("  unsuccessful, please reconnect")
                self.isConnected = False
                self.cntLb.delete(0,10)
                self.connect_button.configure(fg = "black")
                self.rfdConnect

    def rfdDisconnect(self):
        if hasattr(self,'p'):
            self.p.disconnect()
        print "disconnected"
        self.isConnected = False
        self.cntLb.delete(0,10)
        self.connect_button.configure(fg = "black")
        self.temp_label.configure(text="disconnected")


cUUID = "576a7d7f-3db0-44c3-8047-1446bf7c054d"
root = Tk()

scrWidth = root.winfo_screenwidth()
scrHeight = root.winfo_screenheight()
fSize = scrHeight/27
thisFont = tkFont.Font(family="Helvetia",size=fSize)
xOffset = (scrWidth-100)/20

optoGUI = optoGUI(root)
root.after(5000, optoGUI.rfdReceive)
root.mainloop()

#devlist = optorfd.rfdScan
#print("devices found:" + str(devlist))
#p = rfdConnect(devlist,0)
#rfdSend(p, 'AB')

"""
        self.message = "Choose a Device"
        self.label_text = StringVar()
        self.label_text.set(self.message)
        self.label = Label(master, textvariable=self.label_text)

        vcmd = master.register(self.validate)
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.scan_button = Button(master, text="Search", command=self.rfdScan)
        self.connect_button = Button(master, text="Connect", command=self.rfdConnect)

        self.label.grid(row=0, column=0, columnspan=2, stickyh=W+E)
"""
