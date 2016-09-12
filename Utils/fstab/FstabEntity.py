class FstabEntity(object):

    path = ""

    # Sections of the fstab file
    pre = []
    data = {}
    after = []

    def __init__(self, path):
        self.path = path
        self.reset()

    def addToPre(self, line):
        self.pre.append(line)

    def addToAfter(self, line):
        self.after.append(line)

    def reset(self):
        self.pre = []
        self.data = {}
        self.after = []

    def clone(self):
        fstab = FstabEntity(self.path)
        fstab.pre = self.pre
        fstab.currentData = self.currentData
        fstab.after = self.after
        return fstab
