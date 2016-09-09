from UI.GUI import GUI

class EasyMenu(GUI):

    def __init__(self, windowManager, callBack, language):
        super().__init__(windowManager, callBack, language)


    def show(self):
        """
        Init the menu
        """
        self.window.setWindowTitle(self.string["menu"]["title"])
        self.window.removeAll()
        self.window.addLabel(self.string["menu"]["info"])

    def getSshInfo(self):
        return {
            "hostname": self.getInfo(self.string["question"]["get"]["remote_ip"],
                                     tkManager=self.window),
            "username": self.getInfo(self.string["question"]["get"]["remote_user"],
                                     tkManager=self.window),
            "password": self.getPassword(self.string["question"]["get"]["remote_pw"],
                                         tkManager=self.window)
                }

    def getSshfsInfo(self):
        info = self.getSshInfo()
        info["remotePath"] = self.getInfo(self.string["question"]["get"]["remote_path"],
                                          tkManager=self.window)
        info["localPath"] = self.getInfo(self.string["question"]["get"]["local_path"],
                                         tkManager=self.window)
        return info