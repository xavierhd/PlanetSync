from Utils.TkManager import TkManager

class GUI(object):
    def __init__(self, title, callBack):
        self.mainWindow = self.showMenu(title)
        self.callBack = callBack

    def showMenu(self, title):
        tkm = TkManager()
        tkm.addLabel(title)
        return tkm

    def info(self, msg, tkManager=None, isPopup=True):
        tkm = self.getTkManager(tkManager)
        tkm.addLabel(msg)
        if tkm is not self.mainWindow:
            tkm.addButton("Understood!", mustReturn=isPopup)
        if isPopup:
            tkm.run()

    def getPassword(self, msg='Enter your password', tkManager=None, isPopup=True):
        tkm = self.getTkManager(tkManager)
        tkm.addLabel(msg)
        entry = tkm.addEntry(isPassword=True)
        tkm.addButton("Continue", mustReturn=isPopup)
        tkm.run()
        return entry.get()

    def getInfo(self, msg, tkManager=None, isPopup=True):
        tkm = self.getTkManager(tkManager)
        tkm.addLabel(msg)
        entry = tkm.addEntry()
        tkm.addButton("OK", mustReturn=isPopup)
        tkm.run()
        return entry.get()

    def getChoices(self, msg, choices, tkManager=None, isPopup=True):
        """ Choices: array
            Return the chosen's index"""
        tkm = self.getTkManager(tkManager)
        tkm.addLabel(msg)
        for i in range(len(choices)):
            tkm.addButton(choices[i], mustReturn=isPopup, callback=tkm.setAsyncResponse, buttonID=i)
        tkm.run()
        response = tkm.getAsyncResponse()
        return response

    def getTkManager(self, tkManager):
        if tkManager:
            tkm = tkManager
        else:
            tkm = TkManager()
        return tkm
