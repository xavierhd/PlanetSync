
from pprint import pprint
from Utils.SshAgent import SshAgent
from Utils.fstabHandler import Handler


class MainMenu(object):

    gUI = None
    sshAgent = None
    fstabHandler = None

    def __init__(self, gUI, callback):
        self.sshAgent = SshAgent()
        self.fstabHandler = Handler()
        self.gUI = gUI
        self.gUI.showMenu()
        #pprint (self.gUI.string)
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
            info.update(self.gUI.getInfo(self.gUI.string["question"]["share_name"]))
            self.fstabHandler.add(info)
        elif choice == 3:
            print ("Choice 3")
        elif choice == 4:
            print ("Choice 4")