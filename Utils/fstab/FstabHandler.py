
from Utils.fstab.FstabOperation import Operation as FsOperation
from Utils import FileReader


class Handler(FsOperation):
    """
    High level interface with the fstab file
    """

    def __init__(self):
        super().__init__()
        self.refreshCurrentData()

    def getServerList(self):
        """Return the current server listed inside the autogen section"""
        serverList = [key for key in self.fstab.data]
        return serverList

    def getInfo(self, name=None):
        info = None
        if name:
            info = self.fstab.data.get(name)
            info["shareName"] = name
        return info


    def refreshCurrentData(self):
        """
        Update the current data with the fstab autogen section
        """
        self.currentData = self.parseSections(self.fstab)

    def add(self, info, overwrite=False):
        """
        Add a drive to the fstab
        :param info: A dictionnary containing {shareName, username, hostname, remotePath, localPath}
        :param overwrite: allow the overwrite of a share with the same name
        :return: if it has worked
        """
        hasWorked = False
        # Sorry future, i had fun at least
        missing = [item for item in self.fstab.dataRequirement if item not in info]
        if not missing:
            if overwrite or info["shareName"] not in self.fstab.data:
                self.fstab.data[info.pop("shareName")] = info
                hasWorked = True
        else:
            raise AssertionError("Default key/value is missing in parameter <info>: {0}".format(missing))
        return hasWorked


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
