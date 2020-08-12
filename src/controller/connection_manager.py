
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
        self.gui = UI_ConnectionManager(self.window_manager, self.callback, self.language)

    """Override Controller.run"""
    def run(self):
        self.gui.set_closing_operation(self.parent_callback)
        self.gui.show()
        self.gui.set_list(self.gui.primary_list, self.fstabHandler.get_server_list())
        self.gui.run()

    def addShare(self):
        iq = InfoQuery(self.language)
        serverInfo = iq.get_share_info()
        # try ssh connection first

        # add the key in the accepted key list
        if serverInfo:
            # serverInfo == {shareName, username, hostname, remotePath, localPath}
            self.fstabHandler.add(serverInfo)

    """Override Controller.callback"""
    def callback(self, args):
        if args == "back":
            self.callback("back")
        elif args == "addShare":
            self.addShare()
