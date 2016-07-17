class FstabEntity(object):

    path = ""

    preAutogen = []
    currentData = {}
    afterAutogen = []

    def __init__(self, path):
        self.path = path

    def addToPreAutogen(self, line):
        self.preAutogen.append(line)

    def addToAfterAutogen(self, line):
        self.afterAutogen.append(line)

    def clone(self):
        fstab = FstabEntity(self.path)
        fstab.preAutogen = self.preAutogen
        fstab.currentData = self.currentData
        fstab.afterAutogen =self.afterAutogen
        return fstab
