
from Controller import Controller
from UI import EasyMenu as UI_EasyMenu

from Locale import LangSelector as i18n

class EasyMenu(Controller):
    """Operate the UI named EasyMenu"""

    def __init__(self, controller):
        super().__init__(controller=controller)
        self.gUI = UI_EasyMenu(self.windowManager, self.callback)

    """Override Controller.run"""
    def run(self):
        self.gUI.setClosingOperation(self.callBack)
        self.gUI.show()
        self.gUI.run()

    """Override Controller.callback"""
    def callback(self, choice, **args):
        if choice == 0:
            info = self.gUI.getSshfsInfo()
            self.sshAgent.sshfs(info)
        elif choice == 1:
            info = self.gUI.getSshInfo()
            self.sshAgent.addKey(info)
        elif choice == 2:
            info = self.gUI.getSshfsInfo()
            additionalInfo = self.gUI.getInfo(i18n.string["question"]["share_name"])
            info.update(additionalInfo)
            self.fstabHandler.add(info)
        elif choice == 3:
            dic = {
                "shareName": "bob's computer",
                "username": "bob",
                "hostname": "192.146.543.12",
                "remotePath": "/remotePath1/unix/path/spécialChar\\'asd",
                "localPath": "/localPath1/baskd/123hnfk/asld\ asd/pop",
            }
            self.fstabHandler.add(dic)
            self.fstabHandler.save()
        elif choice == 4:
            print ("button #5 pressed")
        elif choice == 5:
            self.callBack("connectionManager")
