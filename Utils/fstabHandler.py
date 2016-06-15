from FilerReader import read

class Handler(object):
    currentData = {}
    inAutoGen = False
    headTemplate, tailTemplate = None

    def __init__(self):
        pass

    def init(self):
        try:
            self.headTemplate = read("UI/Template/head.Template")
            self.tailTemplate = read("UI/Template/tail.Template")
            fstab = read("/etc/fstab")
            key = None
            for line in fstab:
                if self.isAutoGen(line):
                    data = parse(line)
                    if isKey(data):
                        key = data
                    if key and data:
                        self.currentData[key] = data
                        key = None
        except Exception, e:
            raise e

    def parse(self, line):
        if line:
            regex.match("\#\#", line)
            return

    def add(self):
        pass

    def dump(self):
        pass

    def isAutoGen(self, line):
        result = False
        if not self.inAutoGen:
            if line == self.headTemplate:
                self.inAutoGen = True
                result = True
        else:
            result = True
            if line == self.tailTemplate:
                self.inAutoGen = True
                result = False
        return result

    def isKey(self):
        pass

