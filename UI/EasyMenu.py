from UI.GUI import GUI

class EasyMenu(GUI):

    def __init__(self, callBack, language):
        super().__init__(callBack, language)

    def show(self):
        """
        Init the menu
        :return: The window menu instance
        """
        tkm = self.getTkManager(self.window)
        tkm.setCallback(self.callback)
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