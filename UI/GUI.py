from UI.TkManager import TkManager
from UI import LangSelector

class GUI(object):
    mainWindow = None
    string = None

    def __init__(self, callBack, language="english"):
        self.callBack = callBack
        self.string = LangSelector.getLang(language)
        self.mainWindow = self.showMenu()

    def showMenu(self):
        if self.mainWindow:
            tkm = self.mainWindow
        else:
            tkm = TkManager()
        tkm.addLabel(self.string["menu"]["title"])
        tkm.addLabel(self.string["menu"]["info"])
        tkm.addLabel(self.string["menu"]["operation"])
        return tkm

    def getSshInfo(self):
        return  {
            "hostname": self.getInfo(self.string["question"]["get"]["remote_ip"],
                                         tkManager=self.mainWindow),
            "username": self.getInfo(self.string["question"]["get"]["remote_user"],
                                         tkManager=self.mainWindow),
            "password":self.getPassword(self.string["question"]["get"]["remote_pw"],
                                            tkManager=self.mainWindow)
                }

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

    def getChoices(self, msg, choices, tkManager=None, isPopup=False):
        """ Choices: array
            Return the chosen's index"""
        tkm = self.getTkManager(tkManager)
        tkm.removeAll()
        tkm.addLabel(msg)
        for i in range(len(choices)):
            tkm.addButton(choices[i], mustReturn=isPopup, callback=tkm.setAsyncResponse, args=i)
        tkm.run()
        return tkm.getAsyncResponse()

    def getTkManager(self, tkManager):
        if tkManager:
            tkm = tkManager
        else:
            tkm = TkManager()
        return tkm
