
from Controller import Controller
from UI import ConnectionManager as UI_ConnectionManager
from UI.InfoQuery import InfoQuery

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
        self.setListBox(self.gUI.primaryList, self.fstabHandler.getServerList())
        self.gUI.run()

    def setListBox(self, listBox, serverList):
        """
        Set the content of a listbox
        :param listBox: The listBox to be modified
        :param serverList: An array of server to be displayed in the listBox
        """
        self.gUI.setList(listBox, serverList)

    def addToList(self, listBox, newItem):
        """
        Add one item to the provided listBox
        :param listBox: The listbox to be modified
        :param newItem: The element to add to the listbox
        """
        self.gUI.addToList(listBox, newItem)

    def addShare(self):
        import pdb; pdb.set_trace()
        iq = InfoQuery(self.language)
        serverInfo = iq.getShareInfo()
        # serverInfo == {shareName, username, hostname, remotePath, localPath}
        self.fstabHandler.add(serverInfo)

    """Override Controller.callback"""
    def callback(self, args):
        if args == "back":
            self.callBack("back")
        elif args == "addShare":
            self.setListBox(self.gUI.primaryList, args)
