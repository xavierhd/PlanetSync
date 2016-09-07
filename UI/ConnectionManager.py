from UI.TkManager import TkManager
from UI.GUI import GUI
from tkinter import Listbox, END


class ConnectionManager(GUI):
    """
    Interface ayant une liste sélectionnable de serveur.
    Chaque item cliqué affiche la liste des partages associés dans une liste secondaire.
    Un "Double clique?"/"Bouton à droite" sur un item de l'inteface permet de modifier ces informations.
    """

    tkm = None
    primaryList = None
    secondaryList = None

    def __init__(self, windowManager, callback, language):
        super().__init__(windowManager, callback, language)
        self.primaryList = self.tkm.addListbox()
        self.secondaryList = self.tkm.addListbox()

    def show(self):
        """
        Init the window
        :return: The window instance
        """
        self.window.setCallback(self.callback)
        self.window.addLabel(self.string["connectionManager"]["title"])
        self.window.addLabel(self.string["connectionManager"]["info"])
        self.window.addLabel(self.string["connectionManager"]["operation"])

    def setList(self, list, serverList):
        list.delete(0, END)
        for server in serverList:
            list.insert(END, server)

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
