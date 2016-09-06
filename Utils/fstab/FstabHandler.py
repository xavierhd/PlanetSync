
from Utils.fstab.FstabOperation import Operation as FsOperation
from Utils import FileReader


class Handler(FsOperation):
    """
    High level interface with the fstab file
    """

    def __init__(self):
        super().__init__()
        self.refreshCurrentData()

    def refreshCurrentData(self):
        """
        Update the current data with the fstab autogen section
        """
        self.currentData = self.parseSections(self.fstab)

    def add(self, info):
        """
        Add a drive to the fstab
        :param info: A dictionnary containing
        [shareName, username, hostname, remotePath, localPath]
        """
        # TODO: Check if info is already inside
        # Right now the defaut is to overwrite any shared drive having the same name as another
        self.fstab.data[info.pop("shareName")] = info

    def remove(self, shareName):
        """
        Remove a drive from the fstab
        :param shareName: String name of the share (The title in the fstab file)
        """
        result = self.fstab.pop(shareName)
        return result

    def save(self):
        """
        Save the content of the currentData to the fstab file
        """
        self.commit()
