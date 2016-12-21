

from Controller import Controller
from UI import ConnectionManager as UI_ConnectionManager
from UI.InfoQuery import InfoQuery

from Locale import LangSelector as i18n
from Utils import SshAgent

class ConnectionManager(Controller):
    """Control the UI.ConnectionManager"""

    primaryList = None
    secondaryList = None

    def __init__(self, controller):
        super().__init__(controller=controller)
        self.gUI = UI_ConnectionManager(self.windowManager, self.callback)

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
        iq = InfoQuery(root=self.windowManager.tk)
        iq.initGetShareInfo()
        iq.run()
        info = iq.getEntryInfo()
        if info:
            # try an ssh connection first
            # add the key in the accepted key list
            # serverInfo == {shareName, username, hostname, remotePath, localPath}
            self.fstabHandler.add(info)

    def editShare(self, name):
        defautValue = self.fstabHandler.getInfo(name=name)
        iq = InfoQuery(root=self.windowManager.tk, defautlValue=defautValue)
        iq.initGetShareInfo()
        while iq.isAlive:
            iq.run()  # This start the window mainloop
            # "info" is a dict or None if the window havent been closed with the bottom button
            info = iq.getEntryInfo()
            if info:
                iq.isAlive = self.addInfo(info)
        iq.terminate()

    def addInfo(self, info):
        jobDone = False
        userWantToOverwrite = False
        if info:
            # We try to update the fstab with the new info
            jobDone = self.fstabHandler.add(info, overwrite=False)
            if not jobDone:
                userWantToOverwrite = self.gUI.askYesNo(
                    i18n.string["question"]["overwrite"].format(shareName=info["shareName"]),
                    tkManager=self.windowManager)
                if userWantToOverwrite:
                    jobDone = self.fstabHandler.add(info, overwrite=True)
        return jobDone or userWantToOverwrite

    """Override Controller.callback"""
    def callback(self, arg='back', **args):
        if arg == "back":
            self.callBack(arg)
        elif arg == "addShare":
            self.addShare()
        elif arg == "edit":
            self.editShare(args["name"])

        self.setListBox(self.gUI.primaryList, self.fstabHandler.getServerList())

