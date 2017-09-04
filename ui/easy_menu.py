from ui.gui import GUI

from locale import lang_selector as i18n

class EasyMenu(GUI):
    """
    Easy to use interface for beginner
    """

    def __init__(self, windowManager, callBack):
        super().__init__(windowManager, callBack)

    """Override GUI.show"""
    def show(self):
        """
        Init the menu UI component
        """
        self.window.setWindowTitle(i18n.string["menu"]["title"])
        self.window.removeAll()
        self.window.addLabel(i18n.string["menu"]["info"])
        self.getChoices(i18n.string["menu"]["operation"],
                        i18n.string["menu"]["choice"],
                        tkManager=self.window,
                        callBack=self.callBack,
                        append=True)

    def getSshInfo(self):
        """
        Show multiple popup window just like an install wizard,
        asking for mandatory information to make an ssh connection
        """
        return {
            "hostname": self.getInfo(i18n.string["question"]["get"]["remote_ip"],
                                     tkManager=self.window),
            "username": self.getInfo(i18n.string["question"]["get"]["remote_user"],
                                     tkManager=self.window),
            "password": self.getPassword(i18n.string["question"]["get"]["remote_pw"],
                                         tkManager=self.window)
                }

    def getSshfsInfo(self):
        """
        Show multiple popup windows just like an install wizard,
        asking for mandatory information to make an sshfs connection
        """
        info = self.getSshInfo()
        info["remotePath"] = self.getInfo(i18n.string["question"]["get"]["remote_path"],
                                          tkManager=self.window)
        info["localPath"] = self.getInfo(i18n.string["question"]["get"]["local_path"],
                                         tkManager=self.window)
        return info
