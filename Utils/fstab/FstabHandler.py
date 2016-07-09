
from Utils.fstab.FstabOperation import Operation as FsOperation


class Handler(FsOperation):
    """
    High level interface with the fstab file
    """

    def __init__(self):
        self.init()

    def init(self):
        super()
        self.refreshCurrentData()

    def refreshCurrentData(self):
        """
        Update the current data with the fstab autogen section
        """
        self.currentData = self.getAutogenSection()

    def add(self, info):
        """
        Add a drive to the fstab
        :param info: A dictionnary containing
        [shareName, username, hostname, remotePath, localPath]
        """
        self.refreshCurrentData()
        self.currentData[info["shareName"]] = info

    def makeAutogenSection(self, autogenDict):
        """
        Build the fstab autogen section
        :param autogenDict: The data that the fstab file must contain
        """
        autogenString = self.headTemplate
        lineFeed = "\n"
        for key, value in autogenDict.iteritems():
            autogenString += self.entryTemplate.format(key) + lineFeed
