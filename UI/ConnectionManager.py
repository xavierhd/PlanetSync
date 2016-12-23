from tkinter import Listbox, Button, END

from UI.TkManager import TkManager
from UI.GUI import GUI

from Locale import LangSelector as i18n


class ConnectionManager(GUI):
    """
    Interface having a clickable list of server.
    ** Each clicked item show in a second list the associated share.
    A double click/Right click any item open an edition window to change related parameter.
    """

    # Watchout, these are not the UI element, but the content of those
    primaryList = None

    def __init__(self, windowManager, callBack):
        super().__init__(windowManager, callBack)
        self.window.setClosingOperation(callBack)

    """Override GUI.show"""
    def show(self):
        """
        Init the window component
        """
        self.window.setWindowTitle(i18n.string["connectionManager"]["title"])
        self.window.removeAll()
        self.window.addLabel(i18n.string["connectionManager"]["instruction"])
        self.window.addSpacer()

        self.window.addLabel(i18n.string["connectionManager"]["primaryListTitle"])
        buttonSide = Button(self.window.tk,
                            text=i18n.string["connectionManager"]["buttonPrimaryList"],
                            command=self.window.makeLambda([self.callBack], ["addShare"]))
        self.primaryList = self.window.addListbox(buttonSide)
        self.primaryList.bind('<Double-1>', self.listboxEventHandler)

        self.window.addSpacer()
        self.window.addButton(i18n.string["button"]["back"], callBack=self.callBack, args="back")

    def setList(self, targetListbox, newList):
        """
        Set the provided list with the content of the provided serverList
        :param targetListbox: The listbox instance to be setted
        :param newList: An array of new values
        """
        targetListbox.delete(0, END)
        for item in newList:
            self.addToList(targetListbox, item)

    def addToList(self, targetListbox, newItem):
        """
        Add one item to the provided listBox
        :param targetListBox: The listbox to be modified
        :param newItem: The element to add to the listbox
        """
        targetListbox.insert(END, newItem)

    def showAdvanced(self):
        tkm = TkManager()
        tkm.addLabel(i18n.string["advanced"]["title"])
        tkm.addLabel(i18n.string["advanced"]["info"])
        for entry in i18n.string["advanced"]["choices"]:
            pass

    def getSshInfo(self):
        return {
            "hostname": self.getInfo(i18n.string["question"]["get"]["remote_ip"],
                                     tkManager=self.window),
            "username": self.getInfo(i18n.string["question"]["get"]["remote_user"],
                                     tkManager=self.window),
            "password": self.getPassword(i18n.string["question"]["get"]["remote_pw"],
                                         tkManager=self.window)
                }

    def sshfsInfoWindow(self, entry=None):
        tkm = self.getTkManager(None)
        # tkm.addTitle("SSH connection entry")
        tkm.addLabel("Please provide your remote computer's information: ")
        tkm.addLabel(i18n.string["question"]["get"]["remote_ip"])
        entryHostname = tkm.addEntry()
        tkm.addLabel(i18n.string["question"]["get"]["remote_user"])
        entryUsername = tkm.addEntry()
        tkm.addLabel(i18n.string["question"]["get"]["remote_pw"])
        entryPassword = tkm.addEntry(True)
        if entry:
            entryHostname.set(entry["hostname"])
            entryUsername.set(entry["username"])
            entryPassword.set(entry["password"])

        tkm.addButton("Continue", mustReturn=False)
        tkm.run()
        return {"hostname": entryHostname.get(),
                "username": entryUsername.get(),
                "password": entryPassword.get(),
                }

    def mountInfoWindow(self, entry=None):
        tkm = self.getTkManager(None)
        # tkm.addTitle("SSH connection entry")
        tkm.addLabel(i18n.string["question"]["get"]["remote_path"])
        entryRemotePath = tkm.addEntry()
        tkm.addLabel(i18n.string["question"]["get"]["local_path"])
        entryLocalPath = tkm.addEntry()
        if entry:
            entryRemotePath.set(entry["remote_path"])
            entryLocalPath.set(entry["local_path"])

        tkm.addButton("Continue", mustReturn=False)
        tkm.run()
        return {"hostname": entryRemotePath.get(),
                "username": entryLocalPath.get(),
                }

    def listboxEventHandler(self, event):
        listbox = event.widget
        index = int(listbox.curselection()[0])
        self.callBack("edit", name=listbox.get(index))
