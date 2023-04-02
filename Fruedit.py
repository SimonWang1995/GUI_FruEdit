#!/usr/local/bin/python3
from tkinter import *
import re
# from Tkinter.messagebox import showinfo, showwarning
from tkinter.messagebox import *
import os
import subprocess


class window():
    def __init__(self):
        self.root = Tk()
        self.root.title("Fru Edit")
        # self.root.geometry("500x500+100+100")
        fup = Frame(self.root)

        fupleft = Frame(fup, borderwidth=5)
        Label(fupleft, text="IP Address:", borderwidth=5).grid(row=0, column=0, stick=E)
        self.peip = StringVar()
        Entry(fupleft, textvariable=self.peip, width=20).grid(row=0, column=1)
        self.peip.set("localhost")
        # self.peip.set("192.168.0.102")
        Label(fupleft, text="User Name:", borderwidth=5).grid(row=1, column=0, stick=E)
        self.peuser = StringVar()
        Entry(fupleft, textvariable=self.peuser, width=20).grid(row=1, column=1)
        self.peuser.set("admin")
        Label(fupleft, text="Password:", borderwidth=5).grid(row=2, column=0, stick=E)
        self.pepwd = StringVar()
        Entry(fupleft, textvariable=self.pepwd, width=20).grid(row=2, column=1)
        self.pepwd.set("admin")
        fupleft.pack(side=LEFT)
        # +++++++++++++++++++++++++++++===========================
        self.platform = sys.platform
        if self.platform == "linux":
            self.tool = "ipmitool"
        elif self.platform == "win32":
            self.tool = ".\win32\ipmitool.exe"
        fupright = Frame(fup, borderwidth=5)
        Button(fupright, text="Connect", borderwidth=5, width=10, command=self.connect).pack(side=TOP, ipady=3)
        Button(fupright, text="Refresh", borderwidth=5, width=10, command=self.connect).pack(side=BOTTOM, ipady=3)
        fupright.pack(side=RIGHT)
        fup.pack(side=TOP)
        # ===============================================================================================================
        fmiddle = Frame(self.root, borderwidth=5)
        # (row,Name,field,index,length,state)
        self.labellist = [(0, 'FRU Device Description', 'NULL', 'NULL', 0, DISABLED),
                          (1, 'Chassis Type', 'NULL', 'NULL', 0, NORMAL),
                          (2, 'Chassis Part Number', 'c', '0', 12, NORMAL),
                          (3, 'Chassis Serial', 'c', '1', 11, NORMAL),
                          (4, 'Chassis Extra', 'c', '2', 32, NORMAL),
                          (5, 'Board Mfg Date', 'NULL', 'NULL', 0, DISABLED),
                          (6, 'Board Mfg', 'b', '0', 12, NORMAL),
                          (7, 'Board Product', 'b', '1', 16, NORMAL),
                          (8, 'Board Serial', 'b', '2', 10, NORMAL),
                          (9, 'Board Part Number', 'b', '3', 12, NORMAL),
                          (10, 'Product Manufacturer', 'p', '0', 12, NORMAL),
                          (11, 'Product Name', 'p', '1', 32, NORMAL),
                          (12, 'Product Part Number', 'p', '2', 24, NORMAL),
                          (13, 'Product Version', 'p', '3', 6, NORMAL),
                          (14, 'Product Serial', 'p', '4', 24, NORMAL),
                          (15, 'Product Asset Tag', 'p', '5', 32, NORMAL)]
        self.entrylist = []
        for row, name, field, index, length, state in self.labellist:
            Label(fmiddle, borderwidth=5, text=name + " :").grid(row=row, stick=E)
            self.entrylist.append(StringVar())
            Entry(fmiddle, borderwidth=2, textvariable=self.entrylist[row], state=state, width=25).grid(row=row,
                                                                                                        column=1)
            if state != DISABLED:
                a = Button(fmiddle, borderwidth=2, text="Modify",
                           command=lambda name=name, row=row, field=field, index=index, length=length: self.setitem(row,
                                                                                                                    name,
                                                                                                                    field,
                                                                                                                    index,
                                                                                                                    length))
                a.bind("<Return>",
                       lambda event, row=row, field=field, name=name, index=index, length=length: self.setitem(row,
                                                                                                               name,
                                                                                                               field,
                                                                                                               index,
                                                                                                               length))
                a.grid(row=row, column=2)
        fmiddle.pack()
        # ===========================================================================================================================================
        fdown = Frame(self.root, borderwidth=5)
        ab = Button(fdown, text="Set All", command=self.setall)
        ab.bind("<Return>", lambda event: self.setall())
        ab.pack(anchor=CENTER)
        fdown.pack()
        # ===========================================================================================================================================
        framelog = Frame(self.root, borderwidth=5)
        self.log = Text(framelog, height=5, width=50)
        self.log.pack()
        framelog.pack()

    # ===========================================================================================================================================
    def setall(self):
        if self.gettool():
            for row, name, field, index, length, state in self.labellist:
                if row != 0 and row != 1 and row != 5:
                    self.setitem(row, name, field, index, length)

    def gettool(self):
        self.IP = self.peip.get()
        self.user = self.peuser.get()
        self.passwd = self.pepwd.get()
        pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
        if self.IP == "localhost":
            self.ipmitool = self.tool
            state = True
        elif re.match(pattern, self.IP):
            self.ipmitool = self.tool + " -H %s -U %s -P %s" % (self.IP, self.user, self.passwd)
            if self.platform == "win32":
                status = subprocess.call("ping -n 1 %s" % self.peip.get(), shell=True)
                # print "win32 ping status %s" % status
            elif self.platform == "linux":
                status = subprocess.call("ping -c 1 %s" % self.peip.get(), shell=True)
            if status:
                showwarning("Warning", "The host is Lost!")
                state = False
            else:
                state = True
        else:
            showwarning("Warning", "IP address is wrong,\nPlease input again!!")
            state = False
        return state

    def setitem(self, row, name, field, index, length):
        tmp = self.entrylist[row].get()
        cmd = ""
        actuallen = len(tmp)
        if actuallen > length and row != 1:
            showwarning("Warning", "Your Input is too long ( %s Characters )!\n The max length is %s Characters" % (
            actuallen, length))
            return
        if row == 1:
            if tmp not in ["0x17", "0x19", "0x01"]:
                showinfo("Chassis Type Define",
                         "Please enter the chassis type code as bellow:\nRack Mount Chassis : 0x17\n Multi-system Chassis :0x19\n Other :0x01")
                return
        if self.gettool():
            if row == 1:
                self.log.insert(END, "Update " + name + "......\n")
                self.log.see(END)
                self.log.update()
                cmd = "%s raw 0x0a 0x12 0x00 0x5a 0x00 %s " % (self.ipmitool, self.entrylist[row].get())
            else:
                text = tmp + (length - len(tmp)) * " "
                cmd = "%s fru edit 0 field %s %s '%s'" % (self.ipmitool, field, index, text)
                self.log.insert(END, "Update " + name + "......\n")
                self.log.see(END)
                self.log.update()
            result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            while True:
                line = result.stdout.readline()
                self.log.insert(END, str(line.strip()) + "\n")
                self.log.see(END)
                self.log.update()
                if not line:
                    break

    def connect(self):
        if self.gettool():
            row = 0
            cmd = "%s fru list" % self.ipmitool
            print
            cmd
            fruinfo = os.popen(cmd)
            print
            fruinfo
            for line in fruinfo.readlines():
                if line.strip() != "":
                    tmp = line.split(":", 1)[1].strip()
                    self.entrylist[row].set(tmp)
                    row = row + 1
            fruinfo.close()
            showinfo("Tip", "Update have been Completed !")


w = window()
mainloop()


