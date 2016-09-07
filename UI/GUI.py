from UI.TkManager import TkManager
from Locale import LangSelector


class GUI(object):
    """
    Tkinter GUI, high level tools
    """

    window = None
    callback = None
    string = None

    def __init__(self, windowManager, callback, language="english"):
        self.tkm = windowManager
        self.callback = callback
        self.string = LangSelector.getLang(language)
        self.window = windowManager
        self.show()

    def show(self):
        raise TypeError('abstract method must be overridden')

    def info(self, msg, tkManager=None, isPopup=True):
        tkm = self.getTkManager(tkManager)
        tkm.addLabel(msg)
        if tkm is not self.window:
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

    def getChoices(self, title, choices, tkManager=None, isPopup=False, callback=None, append=None):
        """
        Show a list of button choice to the user
        :param choices: array of choices
        :return the chosen index
        """
        tkm = self.getTkManager(tkManager)
        if not append:
            tkm.removeAll()
        if callback is None:
            callback = tkm.setAsyncResponse
        tkm.addLabel(title)

        for i in range(len(choices)):
            tkm.addButton(choices[i], mustReturn=isPopup, callback=callback, args=i)
        if tkManager:
            tkm.run()
        return tkm.getAsyncResponse()

    def getTkManager(self, tkManager=None):
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

    def setCallback(self, callback):
        self.tkm.setCallback(callback)

    def run(self):
        self.tkm.run()

    def terminate(self):
        self.window.destroy()
