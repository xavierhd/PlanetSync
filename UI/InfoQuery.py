
from UI.GUI import GUI
from UI import TkManager

class InfoQuery(GUI):

    def __init__(self, language):
        super().__init__(TkManager(), None, language)

    def getShareInfo(self):
        self.window.addLabel(self.string["question"]["get"]["remote_ip"])
        hostname = self.window.addEntry()

        self.window.addLabel(self.string["question"]["get"]["remote_user"])
        username = self.window.addEntry()

        self.window.addLabel(self.string["question"]["get"]["remote_pw"])
        password = self.window.addEntry(isPassword=True)

        self.window.addLabel(self.string["question"]["get"]["remote_path"])
        remotePath = self.window.addEntry()

        self.window.addLabel(self.string["question"]["get"]["local_path"])
        localPath = self.window.addEntry()
        self.run()
        return {
            "hostname": hostname.get(),
            "username": username.get(),
            "password": password.get(),
            "remotePath": remotePath.get(),
            "localPath": localPath.get(),
            }
