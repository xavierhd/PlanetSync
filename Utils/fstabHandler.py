from FilerReader import read

class Handler(object):
    currentData = {}
    inAutoGen = False
    headTemplate, entryTemplate, tailTemplate= None

    def __init__(self):
        pass

    def init(self):
        try:
            self.headTemplate = read("UI/Template/head.Template")
            self.entryTemplate = read("UI/Template/entry.Template")
            self.tailTemplate = read("UI/Template/tail.Template")
            #fstab = read("/etc/fstab")
            fstab = read("~/test_fstab")
            key = None
            for line in fstab:
                if self.isAutoGenSection(line):
                    data = parse(line)
                    if isKey(data):
                        key = data
                    if key and data:
                        self.currentData[key] = data
                        key = None
        except Exception, e:
            raise e

    def parse(self, line):
        regex = "##->.*<-"
        if line:
            re.split(regex, line)
            return

    def add(self):
        pass

    def dump(self):
        pass

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

    def isKey(self):
        if()
