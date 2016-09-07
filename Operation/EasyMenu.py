
from Operation import Operation
from UI.EasyMenu import EasyMenu as UI_EasyMenu

class EasyMenu(Operation):

    def __init__(self, windowManager, sshAgent, fstabHandler, callback, language):
        super().__init__(callback, sshAgent, fstabHandler)
        self.gUI = UI_EasyMenu(windowManager, callback, language)
        self.gUI.getChoices(self.gUI.string["menu"]["operation"],
                            self.gUI.string["menu"]["choice"],
                            tkManager=self.gUI.window,
                            callback=self.callback,
                            append=True)

    def run(self):
        self.gUI.run()

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
                "shareName": "bob's computer",
                "username": "bob",
                "hostname": "192.146.543.12",
                "remotePath": "/remotePath1/unix/path/spécialChar\\'asd",
                "localPath": "/localPath1/baskd/123hnfk/asld\ asd/pop",
            }
            self.fstabHandler.add(dic)
            self.fstabHandler.save()
        elif choice == 4:
            self.callBack("connectionManager")

    def destroy(self):
        self.gUI.terminate()
