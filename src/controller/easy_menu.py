
from controller import Controller
from user_interface import EasyMenu as UI_EasyMenu

class EasyMenu(Controller):
    """Operate the UI named EasyMenu"""

    def __init__(self, controller):
        super().__init__(controller=controller)
        self.gui = UI_EasyMenu(self.window_manager, self.callback, self.language)

    """Override Controller.run"""
    def run(self):
        self.gui.set_closing_operation(self.parent_callback)
        self.gui.show()
        self.gui.run()

    """Override Controller.callback"""
    def callback(self, choice):
        if choice == 0:
            info = self.gui.get_sshfs_info()
            self.sshAgent.sshfs(info)
        elif choice == 1:
            info = self.gui.get_ssh_info()
            self.sshAgent.addKey(info)
        elif choice == 2:
            info = self.gui.get_sshfs_info()
            share_name = self.gui.get_info(self.gui.string["question"]["get"]["share_name"])
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
            self.parent_callback("connectionManager")
