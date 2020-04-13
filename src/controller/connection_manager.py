
from controller import Controller
from user_interface import ConnectionManager as UI_ConnectionManager
from user_interface.info_query import InfoQuery
from utils import SshAgent

class ConnectionManager(Controller):
    """Control the UI.ConnectionManager"""

    primaryList = None
    secondaryList = None

    def __init__(self, controller):
        super().__init__(controller=controller)
        self.gUI = UI_ConnectionManager(self.windowManager, self.callback, self.language)

    """Override Controller.run"""
    def run(self):
        self.gUI.setClosingOperation(self.callBack)
        self.gUI.show()
        self.gUI.setList(self.gUI.primaryList, self.fstabHandler.getServerList())
        self.gUI.run()

    def addShare(self):
        iq = InfoQuery(self.language)
        serverInfo = iq.getShareInfo()
        # try ssh connection first

        # add the key in the accepted key list
        if serverInfo:
            # serverInfo == {shareName, username, hostname, remotePath, localPath}
            self.fstabHandler.add(serverInfo)

    """Override Controller.callback"""
    def callback(self, args):
        if args == "back":
            self.callBack("back")
        elif args == "addShare":
            self.addShare()
