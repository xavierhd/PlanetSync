from UI.TkManager import TkManager
from UI import LangSelector
from tkinter import Listbox, END


class ConnectionManager(object):
    """
    Interface ayant une liste sélectionnable de serveur.
    Chaque item cliqué affiche la liste des partages associés dans une liste secondaire.
    Un "Double clique?"/"Bouton à droite" sur un item de l'inteface permet de modifier ces informations.
    """

    tkm = None
    primaryList = Listbox()
    secondaryList = Listbox()
    
    callBack = None
    mainWindow = None
    string = None

    def __init__(self, callBack, language="english"):
        self.callBack = callBack
        self.string = LangSelector.getLang(language)
        self.mainWindow = self.showMenu()

    def setPrimaryList(self, serverList):
        self.primaryList.delete(0, END)
        for server in serverList:
            self.primaryList.insert(END, server)

    def showMenu(self):
        """
        Init the menu
        :return: The window menu instance
        """
        if self.mainWindow:
            tkm = self.mainWindow
        else:
            tkm = TkManager(self.callBack)
        tkm.addLabel(self.string["menu"]["title"])
        tkm.addLabel(self.string["menu"]["info"])
        tkm.addLabel(self.string["menu"]["operation"])
        return tkm

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

    def sshInfoWindow(self, entry=None):
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

    def sshfsInfoWindow(self):
        tkm = self.getTkManager(None)

    def getSshfsInfo(self):
        info = self.getSshInfo()
        info["remotePath"] = self.getInfo(self.string["question"]["get"]["remote_path"],
                                          tkManager=self.mainWindow)
        info["localPath"] = self.getInfo(self.string["question"]["get"]["local_path"],
                                         tkManager=self.mainWindow)
        return info

    ##################
    # General method #
    ##################
    def info(self, msg, tkManager=None, isPopup=True):
        tkm = self.getTkManager(tkManager)
        tkm.addLabel(msg)
        if tkm is not self.mainWindow:
            tkm.addButton("Understood!", mustReturn=isPopup)
        if isPopup:
            tkm.run()

    def getPassword(self, msg='Enter your password', tkManager=None, isPopup=False):
        tkm = self.getTkManager(tkManager)
        tkm.removeAll()
        tkm.addLabel(msg)
        entry = tkm.addEntry(isPassword=True)
        tkm.addButton("Continue", mustReturn=isPopup, callback=tkm.setAsyncResponse, args=entry.get)
        tkm.run()
        return tkm.getAsyncResponse()

    def getInfo(self, msg, tkManager=None, isPopup=False):
        tkm = self.getTkManager(tkManager)
        tkm.removeAll()
        tkm.addLabel(msg)
        entry = tkm.addEntry()
        tkm.addButton("Continue", mustReturn=isPopup, callback=tkm.setAsyncResponse, args=entry.get)
        tkm.run()
        return tkm.getAsyncResponse()

    def getChoices(self, title, choices, tkManager=None, isPopup=False, callback=None):
        """
        Choices: array of choices
        :return the chosen index
        """
        tkm = self.getTkManager(tkManager)
        tkm.removeAll()
        if callback is None:
            callback = tkm.setAsyncResponse
        tkm.addLabel(title)

        for i in range(len(choices)):
            tkm.addButton(choices[i], mustReturn=isPopup, callback=callback, args=i)
        tkm.run()
        return tkm.getAsyncResponse()

    def getTkManager(self, tkManager):
        """
        Get a tkManager instance. If the param is None, return a new TkManager
        :param tkManager: should contain a tkManager instance.
        :return: a tkManager
        """
        if tkManager:
            tkm = tkManager
        else:
            tkm = TkManager()
        return tkm

    def terminate(self):
        self.mainWindow.destroy()
