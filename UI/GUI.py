from UI.TkManager import TkManager
from Locale import LangSelector


class GUI(object):
    """
    Tkinter GUI, high level tools
    """

    window = None
    callBack = None
    string = None

    def __init__(self, windowManager, callBack, language="english"):
        """
        :param windowManager: An instance of TkManager
        :param callBack: A function to be bind button to
        :param language: The language to use, TODO: Deprecate this
        """
        self.callBack = callBack
        self.string = LangSelector.getLang(language)
        self.window = windowManager

    def show(self):
        raise NotImplementedError('abstract method must be overridden')

    def info(self, text, tkManager=None):
        """
        :param text: The text to display
        :param tkManager: An instance of TkManager. If no manager is given, a the info will be displayed as a popup
        """
        tkm = self.getTkManager(tkManager)
        tkm.addLabel(text)
        if not tkManager:
            tkm.addButton("Understood!", mustReturn=True, callBack=tkm.quit())
            tkm.run()

    def getPassword(self, text='Enter your password', tkManager=None):
        """
        Show an obfuscated entrybox to let user input password
        :param text: The text to display as a hint over the password field
        :param tkManager: An instance of TkManager. If no manager, a popup is used instead
        :return: The password field / Popup: The password input by the user
        """
        tkm = self.getTkManager(tkManager)
        tkm.removeAll()
        tkm.addLabel(text)
        entry = tkm.addEntry(isPassword=True)
        if not tkManager:
            tkm.addButton("Continue", mustReturn=True, callBack=tkm.setAsyncResponse, args=entry.get)
            tkm.run()
            return tkm.getAsyncResponse()
        else:
            return entry

    def getInfo(self, text, tkManager=None):
        """
        Show an entrybox to let the user input information
        :param text: The text to display as a hint over the info field
        :param tkManager: An instance of TkManager. If no manager, a popup is used instead
        :return: The info field / Popup: The info input by the user
        """
        tkm = self.getTkManager(tkManager)
        tkm.removeAll()
        tkm.addLabel(text)
        entry = tkm.addEntry()
        if not tkManager:
            tkm.addButton("Continue", mustReturn=True, callBack=tkm.setAsyncResponse, args=entry.get)
            tkm.run()
            return tkm.getAsyncResponse()
        else:
            return entry

    def getChoices(self, title, choices, tkManager=None, callBack=None, append=None):
        """
        Show a list of button choice to the user
        :param choices: array of choices
        :return: The index of the clicked button
        """
        isPopup = True if tkManager else False
        tkm = self.getTkManager(tkManager)
        if not append:
            tkm.removeAll()
        if not callBack:
            callBack = self.setAsyncResponse

        tkm.addLabel(title)
        for i in range(len(choices)):
            tkm.addButton(choices[i], mustReturn=isPopup, callBack=callBack, args=i)
        if not tkManager:
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
        """
        Set the callback for closing operation
        """
        self.window.setClosingOperation(callback)

    def run(self):
        """
        Init the window component and run the UI main loop
        """
        self.show()
        self.window.run()

    def terminate(self):
        """
        Put an end to all this crazyness
        """
        self.window.destroy()
