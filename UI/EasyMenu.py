from UI.GUI import GUI

class EasyMenu(GUI):
    """
    Easy to use interface for beginner
    """

    def __init__(self, windowManager, callBack, language):
        super().__init__(windowManager, callBack, language)

    """Override GUI.show"""
    def show(self):
        """
        Init the menu UI component
        """
        self.window.setWindowTitle(self.string["menu"]["title"])
        self.window.removeAll()
        self.window.addLabel(self.string["menu"]["info"])
        self.getChoices(self.string["menu"]["operation"],
                            self.string["menu"]["choice"],
                            tkManager=self.window,
                            callback=self.callBack,
                            append=True)

    def getSshInfo(self):
        """
        Show multiple popup window just like an install wizard,
        asking for mandatory information to make an ssh connection
        """
        return {
            "hostname": self.getInfo(self.string["question"]["get"]["remote_ip"],
                                     tkManager=self.window),
            "username": self.getInfo(self.string["question"]["get"]["remote_user"],
                                     tkManager=self.window),
            "password": self.getPassword(self.string["question"]["get"]["remote_pw"],
                                         tkManager=self.window)
                }

    def getSshfsInfo(self):
        """
        Show multiple popup windows just like an install wizard,
        asking for mandatory information to make an sshfs connection
        """
        info = self.getSshInfo()
        info["remotePath"] = self.getInfo(self.string["question"]["get"]["remote_path"],
                                          tkManager=self.window)
        info["localPath"] = self.getInfo(self.string["question"]["get"]["local_path"],
                                         tkManager=self.window)
        return info
