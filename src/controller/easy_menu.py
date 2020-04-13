
from controller import Controller
from user_interface import EasyMenu as UI_EasyMenu

class EasyMenu(Controller):
    """Operate the UI named EasyMenu"""

    def __init__(self, controller):
        super().__init__(controller=controller)
        self.gUI = UI_EasyMenu(self.windowManager, self.callback, self.language)

    """Override Controller.run"""
    def run(self):
        self.gUI.setClosingOperation(self.callBack)
        self.gUI.show()
        self.gUI.run()

    """Override Controller.callback"""
    def callback(self, choice):
        if choice == 0:
            info = self.gUI.getSshfsInfo()
            self.sshAgent.sshfs(info)
        elif choice == 1:
            info = self.gUI.getSshInfo()
            self.sshAgent.addKey(info)
        elif choice == 2:
            info = self.gUI.getSshfsInfo()
            share_name = self.gUI.getInfo(self.gUI.string["question"]["get"]["share_name"])
            info.update({"shareName": share_name})
            self.fstabHandler.add(info)
        elif choice == 3:
            dic = {
                "shareName": "bob's computer",
                "username": "xavier",
                "hostname": "127.0.0.1",
                "remotePath": "/remotePath1/unix/path/specialChar\\'asd",
                "localPath": "/localPath1/baskd/123hnfk/asld\ asd/pop",
            }
            self.fstabHandler.add(dic)
            self.fstabHandler.save()
        elif choice == 4:
            print ("button #5 pressed")
        elif choice == 5:
            self.callBack("connectionManager")
