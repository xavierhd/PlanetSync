
from UI.GUI import GUI
from UI import TkManager

class InfoQuery(GUI):

    isAlive = True

    def __init__(self, language):
        super().__init__(TkManager(), None, language)
        self.setClosingOperation(self.quit)

    def getShareInfo(self):
        self.window.addLabel(self.string["question"]["get"]["share_name"])
        shareName = self.window.addEntry()

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
        self.window.addSpacer()
        self.window.addButton(self.string["general"]["buttonAdd"], mustReturn=True)
        self.run()
        info = None
        if self.isAlive:
            info =  {
                "shareName": shareName.get(),
                "hostname": hostname.get(),
                "username": username.get(),
                "password": password.get(),
                "remotePath": remotePath.get(),
                "localPath": localPath.get(),
                }
            # Make sure that this tkManager is dead
            self.terminate()
        return info


    def quit(self):
        self.isAlive = False
        self.terminate()
