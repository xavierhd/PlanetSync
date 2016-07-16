from Utils.SshAgent import SshAgent
from Utils.fstab.FstabHandler import Handler


class MainMenu(object):

    gUI = None
    sshAgent = None
    fstabHandler = None

    def __init__(self, gUI, callback):
        self.sshAgent = SshAgent()
        self.fstabHandler = Handler()
        self.gUI = gUI
        self.gUI.showMenu()
        # pprint (self.gUI.string)
        self.gUI.getChoices(self.gUI.string["menu"]["operation"],
                            self.gUI.string["menu"]["choice"],
                            tkManager=self.gUI.mainWindow,
                            callback=self.callback)

    def callback(self, choice):
        if choice == 0:
            info = self.gUI.getSshfsInfo()
            self.sshAgent.sshfs(info)
        elif choice == 1:
            info = self.gUI.getSshInfo()
            self.sshAgent.addKey(info)
        elif choice == 2:
            info = self.gUI.getSshfsInfo()
            additionalInfo = self.gUI.getInfo(self.gUI.string["question"]["share_name"])
            info.update(additionalInfo)
            self.fstabHandler.add(info)
        elif choice == 3:
            dic = {
                "shareName": "shareName1",
                "username": "username1",
                "hostname": "hostname1",
                "remotePath": "remotePath1",
                "localPath": "localPath1",
            }
            self.fstabHandler.add(dic)
            self.fstabHandler.save()
        elif choice == 4:
            print ("Choice 4")