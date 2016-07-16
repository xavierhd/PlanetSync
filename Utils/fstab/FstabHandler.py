
from Utils.fstab.FstabOperation import Operation as FsOperation
from Utils import FileReader


class Handler(FsOperation):
    """
    High level interface with the fstab file
    """

    def __init__(self):
        self.init()

    def init(self):
        super().__init__()
        self.refreshCurrentData()

    def refreshCurrentData(self):
        """
        Update the current data with the fstab autogen section
        """
        self.currentData = self.parseSections()
        print (self.currentData)

    def add(self, info):
        """
        Add a drive to the fstab
        :param info: A dictionnary containing
        [shareName, username, hostname, remotePath, localPath]
        """
        # TODO: Check if info is already inside
        self.currentData[info["shareName"]] = info

    def remove(self, shareName):
        """
        Remove a drive from the fstab
        :param shareName: String name of the share (The title in the fstab file)
        """
        result = self.currentData.pop(shareName)
        return result

    def save(self):
        """
        Save the content of the currentData to the fstab file
        """
        self.commit()
