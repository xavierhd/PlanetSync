from UI.TkManager import TkManager
from UI.GUI import GUI
from tkinter import Listbox, Button, END


class ConnectionManager(GUI):
    """
    Interface having a clickable list of server.
    Each clicked item show in a second list the associated share.
    A double click/Right click any item open an edition window to change related parameter.
    """

    # Watchout, these are not the UI element, but the content of those
    primaryList = None
    secondaryList = None

    def __init__(self, windowManager, callBack, language):
        super().__init__(windowManager, callBack, language)

    """Override GUI.show"""
    def show(self):
        """
        Init the window component
        """
        self.window.setWindowTitle(self.string["connectionManager"]["title"])
        self.window.removeAll()
        self.window.addLabel(self.string["connectionManager"]["instruction"])
        self.window.addSpacer()

        self.window.addLabel(self.string["connectionManager"]["primaryListTitle"])
        self.primaryList = self.window.addListbox()
        self.window.addSpacer()

        self.window.addLabel(self.string["connectionManager"]["secondaryListTitle"])
        buttonSecondaryList = Button(self.window.tk,
            text=self.string["connectionManager"]["buttonSecondaryList"],
            command=self.window.makeLambda(self.callBack, "addShare"))
        self.secondaryList = self.window.addListbox(buttonSecondaryList)
        self.window.addSpacer()
        self.window.addButton(self.string["general"]["buttonBack"], callBack=self.callBack, args="back")

    def addToList(self, targetListbox, newItem):
        targetListbox.insert(END, newItem)

    def setList(self, targetListbox, serverList):
        """
        Set the provided list with the content of the provided serverList
        :param targetListbox: The listbox instance to be setted
        :param serverList: An array of new values
        """
        targetListbox.delete(0, END)
        for server in serverList:
            targetListbox.insert(END, server)

    def showAdvanced(self):
        tkm = TkManager()
        tkm.addLabel(self.string["advanced"]["title"])
        tkm.addLabel(self.string["advanced"]["info"])
        for entry in self.string["advanced"]["choices"]:
            pass

    def getSshInfo(self):
        return {
            "hostname": self.getInfo(self.string["question"]["get"]["remote_ip"],
                                     tkManager=self.window),
            "username": self.getInfo(self.string["question"]["get"]["remote_user"],
                                     tkManager=self.window),
            "password": self.getPassword(self.string["question"]["get"]["remote_pw"],
                                         tkManager=self.window)
                }

    def sshfsInfoWindow(self, entry=None):
        tkm = self.getTkManager(None)
        # tkm.addTitle("SSH connection entry")
        tkm.addLabel("Please provide your remote computer's information: ")
        tkm.addLabel(self.string["question"]["get"]["remote_ip"])
        entryHostname = tkm.addEntry()
        tkm.addLabel(self.string["question"]["get"]["remote_user"])
        entryUsername = tkm.addEntry()
        tkm.addLabel(self.string["question"]["get"]["remote_pw"])
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
        tkm.addLabel(self.string["question"]["get"]["remote_path"])
        entryRemotePath = tkm.addEntry()
        tkm.addLabel(self.string["question"]["get"]["local_path"])
        entryLocalPath = tkm.addEntry()
        if entry:
            entryRemotePath.set(entry["remote_path"])
            entryLocalPath.set(entry["local_path"])

        tkm.addButton("Continue", mustReturn=False)
        tkm.run()
        return {"hostname": entryRemotePath.get(),
                "username": entryLocalPath.get(),
                }
