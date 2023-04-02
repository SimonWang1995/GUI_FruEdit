#!/usr/bin/python3
from tkinter import *
import re
from tkinter.messagebox import *
import os
from threading import Thread
import subprocess

"""
    Inventec FAE
    Author: Simon Wang
    Modify Date: 2022/04/13
    Description:
    Fru Edit GUI Kit, Without Extra
"""


_HOME_PATH = os.path.dirname(__file__)


class LoginPage:
    def __init__(self, master=None):
        self.root = master
        self.root.geometry('%dx%d' % (300, 180))
        self.bmcip = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.platform = sys.platform
        if self.platform == "linux":
            self.tool = "ipmitool"
        elif self.platform == "win32":
            self.tool = os.path.join(_HOME_PATH, "win32" + os.sep + "ipmitool.exe")
        self.IPMI = ""
        self.createpage()

    def createpage(self):
        self.page = Frame(self.root)
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='IP地址: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.bmcip).grid(row=1, column=1, stick=E)
        Label(self.page, text='账户: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=2, column=1, stick=E)
        Label(self.page, text='密码: ').grid(row=3, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=3, column=1, stick=E)
        Button(self.page, text='登陆', command=lambda tool=self.tool: self.logincheck(tool)).grid(row=4, stick=W, pady=10)
        Button(self.page, text='退出', command=self.page.quit).grid(row=4, column=1, stick=E)

    def logincheck(self, tool):
        ip = self.bmcip.get()
        name = self.username.get()
        secret = self.password.get()
        pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
        if ip == "localhost":
            self.IPMI = self.tool
            self.page.destroy()
            MainPage(self.root, self.IPMI, ip).getfru()
        else:
            res, msg = self.check_ip(ip)
            if not res:
                showwarning('Warning', msg)
            elif len(name) != 0 and len(secret) != 0:
                self.IPMI = self.tool + " -H %s -U %s -P %s " % (ip, name, secret)
                #cmd=self.IPMI+"fru print"
                if self.check_cmd(cmd=self.IPMI+"fru print"):
                    self.page.destroy()
                    MainPage(self.root, self.IPMI, ip).getfru()
                else:
                    showinfo(title='错误', message="无法获取Fru，请检查IP、账号和密码！")
            else:
                showinfo(title='错误', message='账号或密码错误！')
#        print(self.IPMI)

    @staticmethod
    def check_cmd(cmd):
        subpro = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if subpro.stderr.readlines():
            return False
        else:
            return True

    @staticmethod
    def check_ip(ip):
        res = False
        msg = ""
        ping_cmd = ""
        pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
        if re.match(pattern, ip):
#            self.ipmitool = self.tool + " -H %s -U %s -P %s" % (self.IP, self.user, self.passwd)
            if sys.platform == "win32":
                ping_cmd = "ping -n 1 {}".format(ip)
                # print "win32 ping status %s" % status
            elif sys.platform == "linux":
                ping_cmd = "ping -c 1 {}".format(ip)
            status = subprocess.call(ping_cmd, shell=True)
            if status:
                # showwarning("Warning", "The host is Lost!")
                res = False
                msg = "Can't Ping BMC IP Address: {}".format(ip)
            else:
                res = True
        else:
            # showwarning("Warning", "IP address is wrong,\nPlease input again!!")
            res = False
            msg = "Wrong BMC Ip Address: {}".format(ip)
        return res, msg


class MainPage:
    def __init__(self, master=None, tool=None, ip=None):
        self.IP = ip
        self.ipmitool = tool
        self.Result = {}
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (500, 600))  # 设置窗口大小
        self.createpage()

    def createpage(self):
        fmiddle = Frame(self.root, borderwidth=5)
        # (row,Name,field,index,length,state)
        self.labellist = [(0, 'FRU Device Description', 'NULL', 'NULL', 0, DISABLED),
                          (1, 'Chassis Type', 'NULL', 'NULL', 0, DISABLED),
                          (2, 'Chassis Part Number', 'c', '0', 12, NORMAL),
                          (3, 'Chassis Serial', 'c', '1', 11, NORMAL),
                          (4, 'Chassis Extra', 'c', '2', 32, NORMAL),
                          (5, 'Board Mfg Date', 'NULL', 'NULL', 0, DISABLED),
                          (6, 'Board Mfg', 'b', '0', 12, DISABLED),
                          (7, 'Board Product', 'b', '1', 16, NORMAL),
                          (8, 'Board Serial', 'b', '2', 10, NORMAL),
                          (9, 'Board Part Number', 'b', '3', 12, NORMAL),
                          (10, 'Product Manufacturer', 'p', '0', 12, DISABLED),
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
        Button(fdown, text="Refresh", command=self.getfru).grid(row=0, column=0, padx=100)
        ab = Button(fdown, text="Set All", command=self.setall)
        ab.bind("<Return>", lambda event: self.setall())
        ab.grid(row=0, column=1, padx=100)
        fdown.pack()
        # ===========================================================================================================================================
        framelog = Frame(self.root, borderwidth=5)
        self.log = Text(framelog, height=10, width=50)
        self.log.pack(expand=YES)
        framelog.pack(expand=YES)

        # ===========================================================================================================================================
    def setitem(self, row, name, field, index, length):
#        if LoginPage.check_ip(self,self.IP):
        tmp = self.entrylist[row].get()
        cmd = ""
        actuallen = len(tmp)
        if actuallen > length and row != 1:
            showwarning("Warning", "Your Input is too long ( %s Characters )!\n The max length is %s Characters" % (
                actuallen, length))
            return
        else:
            text = tmp + (length - len(tmp)) * " "
            cmd = "%s fru edit 0 field %s %s '%s'" % (self.ipmitool, field, index, text)
            self.log.insert(END, "Update " + name + "......\n")
            self.log.see(END)
            self.log.update()
        res = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        # stdout,stderr=res.communicate()
        # print(stderr)
        # print(stdout)
        while True:
            line = res.stdout.readline()
            self.log.insert(END, str(line.strip()) + "\n")
            self.log.see(END)
            self.log.update()
            if not line:
                break
        if res.stderr.readlines():
            self.Result[name] = "Fail"
            self.log.insert(END, "Update " + name + " Failed \n\n")
        else:
            self.Result[name] = "Pass"
            self.log.insert(END, "Update " + name + " Passed \n\n")

    def setall(self):
        self.Result.clear()
        res, msg = LoginPage.check_ip(self.IP)
        if res:
            threadlist = []
            for row, name, field, index, length, state in self.labellist:
                if state != DISABLED:
                    #self.setitem(row, name, field, index, length)
                    t = Thread(self.setitem(row, name, field, index, length))
                    t.start()
                    threadlist.append(t)
            for t in threadlist:
                t.join()
 #           print(self.Result)
#            showinfo("Tip", "Update have been Completed !")
            for key, value in self.Result.items():
                self.log.insert(END, key+":"+value+"\n")
            showinfo("Result", "Update have been Completed!,See window Event log for result")
        else:
            showwarning('Warning', msg)

    def getfru(self):
        res, msg = LoginPage.check_ip(self.IP)
        if res:
            row = 0
            cmd = "%s fru list" % self.ipmitool
            fruinfo = os.popen(cmd)
            # showinfo(message=cmd)
            # fruinfo=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            # fruinfo.wait()
            # # stdout, stderr = p.communicate()
            # showinfo(message=fruinfo.stderr)
            # # open("frufile.txt",'w').writelines(str(stdout))
            for line in fruinfo.readlines():
                if line.strip() != "":
                    tmp = line.split(":", 1)[1].strip()
                    self.entrylist[row].set(tmp)
                    row = row + 1
            # statu=fruinfo.wait()
            fruinfo.close()
            showinfo("Tip", "Refresh have been Completed !")
        else:
            showwarning('Warning', msg)


if __name__ == "__main__":
    root = Tk()
    root.title("FruEdit")
    LoginPage(root)
    root.mainloop()