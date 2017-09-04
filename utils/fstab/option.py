from os.path import expanduser, dirname, abspath
from utils.file_reader import readYaml


class Option(object):
    """
    Option handler
    """
    option = None

    def __init__(self):
        self.option = readYaml("./option.yaml")

    def getAll(self):
        allOptions = {}
        allOptions.update(self.getFlag())
        allOptions.update(self.getChoice())
        allOptions.update(self.getNumber())
        allOptions.update(self.getString())
        return allOptions

    def getFlag(self):
        return self.option["flag"]

    def getChoice(self):
        return self.option["choice"]

    def getNumber(self):
        return self.option["number"]

    def getString(self):
        return self.option["string"]
