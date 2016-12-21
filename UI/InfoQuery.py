
from UI.GUI import GUI
from UI import TkManager

from Locale import LangSelector as i18n

class InfoQuery(GUI):

    isAlive = True
    shareName = None
    hostname = None
    username = None
    remotePath = None
    localPath = None
    password = None

    def __init__(self, root=None, defautlValue=None):
        super().__init__(TkManager(root=root), None)
        self.defaultValue = defautlValue
        self.setClosingOperation(self.quit)

    def initGetShareInfo(self):
        self.isAlive = True
        self.window.removeAll()
        self.window.addLabel(i18n.string["question"]["get"]["share_name"])
        self.shareName = self.window.addEntry()

        self.window.addLabel(i18n.string["question"]["get"]["remote_ip"])
        self.hostname = self.window.addEntry()

        self.window.addLabel(i18n.string["question"]["get"]["remote_user"])
        self.username = self.window.addEntry()

        self.window.addLabel(i18n.string["question"]["get"]["remote_pw"])
        self.password = self.window.addEntry(isPassword=True)

        self.window.addLabel(i18n.string["question"]["get"]["remote_path"])
        self.remotePath = self.window.addEntry()

        self.window.addLabel(i18n.string["question"]["get"]["local_path"])
        self.localPath = self.window.addEntry()
        self.window.addSpacer()
        self.window.addButton(i18n.string["button"]["add"], mustReturn=1, callBack=self.getEntryInfo)

        if self.defaultValue:  # {shareName, username, hostname, remotePath, localPath}
            self.shareName.insert(0, self.defaultValue["shareName"])
            self.hostname.insert(0, self.defaultValue["hostname"])
            self.username.insert(0, self.defaultValue["username"])
            self.remotePath.insert(0, self.defaultValue["remotePath"])
            self.localPath.insert(0, self.defaultValue["localPath"])

    def getEntryInfo(self):
        if self.isAlive:
            return {
                "shareName": self.shareName.get(),
                "hostname": self.hostname.get(),
                "username": self.username.get(),
                "password": self.password.get(),
                "remotePath": self.remotePath.get(),
                "localPath": self.localPath.get(),
            }

    def quit(self):
        self.isAlive = False
        self.terminate()

"""##transient is only part of the solution. You also want to set the grab on the
##secondary window, and then wait for the secondary window to close.
##So this is the magical sequence to make a window modal in Tkinter:
##transient, grab_set, wait_window. -Eric Brunel

from tkinter import *


def go():
    wdw = Toplevel()
    wdw.geometry('+400+400')
    e = Entry(wdw)
    e.pack()
    e.focus_set()
    wdw.transient(root)
    wdw.grab_set()
    root.wait_window(wdw)
    print('done!')

root = Tk()
Button(root, text='Go', command=go).pack()
Button(root, text='Quit', command=root.destroy).pack()
root.mainloop()"""