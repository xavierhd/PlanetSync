from Utils.FileReader import read


class Handler(object):
    currentData = {}
    inAutoGen = False
    headTemplate, entryTemplate, tailTemplate= None
    FSTAB_FILE = "~/test_fstab"

    def __init__(self):
        self.init()

    def init(self):
        self.inAutoGen = False
        try:
            self.headTemplate = read("UI/Template/head.Template")
            self.entryTemplate = read("UI/Template/entry.Template")
            self.tailTemplate = read("UI/Template/tail.Template")
            # fstab = read("/etc/fstab")
            self.currentData = self.getAutogenSection()
        except Exception as e:
            raise e

    def add(self, info):
        self.inAutoGen = False
        output = []
        fstab = read(self.FSTAB_FILE)
        for line in fstab:
            if line:
                if not self.isAutoGenSection(line):
                    output.append(line)

    def isAutoGenSection(self, line):
        """
        Check if the line is inside the autogen section
        """
        result = False

        if not self.inAutoGen:
            if self.isHead(line):
                result = True
        else:
            if not self.isTail(line):
                result = True

        return result

    def isHead(self, line):
        """
        Check if the line is the head of the autogen section
        """
        result = False
        if line == self.headTemplate:
            self.inAutoGen = True
            result = True
        return result

    def isTail(self, line):
        """
        Check if the line is the tail of the autogen section
        """
        result = False
        if line == self.tailTemplate:
            self.inAutoGen = False
            result = True
        return result

    def getKey(self, line):
        key = None
        regex = "##->"
        if line:
            split = re.split(regex, line)
            if split.lenght >=2:
                key = split[1]
        return key

    def getAutogenSection(self):
        autogenSection = {}
        fstab = read(self.FSTAB_FILE)
        key = None

        for line in fstab:
            if line:
                if self.isAutoGenSection(line):
                    if not key:
                        key = self.getKey(line)
                    else:
                        autogenSection[key] = line
                        key = None
        return autogenSection

    def makeAutogenSection(self, autogenDict):
        autogenString = self.headTemplate
        lineFeed = "\n"
        for key, value in autogenSection.iteritems():
            autogenString += self.entryTemplate.format(key) + lineFeed