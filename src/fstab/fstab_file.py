from fstab.fstab_parser import FstabParser

class FstabFile(FstabParser):

    def __init__(self, path):
        super().__init__(path)

    def clone(self):
        fstab = FstabFile(self.path)
        fstab.head = self.head
        fstab.entries = self.entries
        fstab.tail = self.tail
        return fstab

    def get_server_list(self):
        """Return the current servers listed inside the autogen section"""
        return [entry_key for entry_key in self.entries]

    def add(self, info):
        """
        Add a drive to the fstab
        :param info: A dictionnary containing object with attributes {shareName, username, hostname, remotePath, localPath}
        """
        # TODO: Check if info is already inside
        # Right now the defaut is to overwrite any shared drive having the same name as another
        self.entries[info.pop("shareName")] = info

    def remove(self, shareName):
        """
        Remove a drive from the fstab
        :param shareName: String name of the share (The title in the fstab file)
        """
        result = self.entries.pop(shareName)
        return result
