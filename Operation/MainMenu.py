
from pprint import pprint

class MainMenu(object):

    gUI = None

    def __init__(self, gUI, callback):
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
