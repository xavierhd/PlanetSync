from UI.TkManager import TkManager
from UI import LangSelector
from UI.GUI import GUI
from tkinter import Listbox, END


class ConnectionManager(GUI):
    """
    Interface ayant une liste sélectionnable de serveur.
    Chaque item cliqué affiche la liste des partages associés dans une liste secondaire.
    Un "Double clique?"/"Bouton à droite" sur un item de l'inteface permet de modifier ces informations.
    """

    tkm = None
    window = None
    primaryList = None
    secondaryList = None

    def __init__(self, callBack, language):
        super().__init__(callBack, language)
        self.primaryList = self.tkm.addListBox()
        self.secondaryList = self.tkm.addListBox()
        self.window = self.show()

    def show(self):
        """
        Init the window
        :return: The window instance
        """
        if self.window:
            tkm = self.window
        else:
            tkm = TkManager(self.callBack)
        tkm.addLabel(self.string["connectionManager"]["title"])
        tkm.addLabel(self.string["connectionManager"]["info"])
        tkm.addLabel(self.string["connectionManager"]["operation"])
        return tkm

    def setList(self, list, serverList):
        self.list.delete(0, END)
        for server in serverList:
            self.list.insert(END, server)

    def showAdvanced(self):
        tkm = TkManager()
        tkm.addLabel(self.string["advanced"]["title"])
        tkm.addLabel(self.string["advanced"]["info"])
        for entry in self.string["advanced"]["choices"]:
            pass

    def getSshInfo(self):
        return {
            "hostname": self.getInfo(self.string["question"]["get"]["remote_ip"],
                                     tkManager=self.mainWindow),
            "username": self.getInfo(self.string["question"]["get"]["remote_user"],
                                     tkManager=self.mainWindow),
            "password": self.getPassword(self.string["question"]["get"]["remote_pw"],
                                         tkManager=self.mainWindow)
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

    def sshfsInfoWindow(self):
        tkm = self.getTkManager(None)

    def terminate(self):
        self.mainWindow.destroy()
