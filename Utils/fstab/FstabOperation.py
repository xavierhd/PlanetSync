from os.path import expanduser, dirname, abspath
import re # regex utility

from Utils.FileReader import read, readLine, dump

from Utils.fstab.FstabEntity import FstabEntity


class Operation(object):
    """
    Low level interface with the fstab file
    """

    fstab = None

    inAutoGen = False

    # Template of the autogenerated section
    headTemplate = None
    entryTemplate = None
    tailTemplate = None

    def __init__(self):
        self.loadTemplate()
        self.fstab = FstabEntity(expanduser("~")+"/test_fstab")


    def getKey(self, line):
        key = None
        regex = "##"
        if line:
            split = re.split(regex, line)
            if len(split) >= 2:
                key = split[1]
        return key

    def parseSections(self, fstabEntity):
        """
        Parse the fstab into 3 sections: preAutogen, autogen and afterAutogen
        :param fstabEntity: An fstab object made of a FstabEntity
        :return: the autogenerated section of the fstab file
        """
        autogenSection = {}
        fstab = readLine(fstabEntity.path)
        key = None
        fstabEntity.reset()
        # If read have returned something
        if fstab:
            for line in fstab:

                # If we are inside the autogen section and the line isn't empty (in fact a nextLine char)
                if line != "/n" and self.isAutoGenSection(line):

                    # Make sure that the first run doesn't try to find a key in headTemplate
                    if self.inAutoGen:
                        # If there is no key, we try to find one
                        if not key:
                            # Remove the nextLine character from the line
                            line = line[:len(line)-1]
                            key = self.getKey(line)
                        # We use the key to link the line to it
                        else:
                            autogenSection[key] = line
                            key = None
                    else:
                        self.inAutoGen = True

                # If we are outside and before of autogen section
                elif not self.inAutoGen and not fstabEntity.data:
                    fstabEntity.addToPre(line)

                # If we are outside and after of autogen section
                elif not self.inAutoGen and fstabEntity.data:
                    fstabEntity.addToAfter(line)

                # If none of the case before are True, we reset the state of the parsing to "not in autogen".
                # This case happen right after isAutoGenSection() return false, while self.inAutoGen is True. -> when "line" == "tail.template"
                else:
                    self.inAutoGen = False
        fstabEntity.data = self.parseData(autogenSection)
        return fstabEntity.data

    def parseData(self, dataSection):
        """
        Parse the raw data from the fstab's autogen retrieved section
        """
        data = {}
        pattern = re.compile(r"#(?P<username>(?:[A-z._])\w+)") # @(?P<hostname>(?:[A-z._])\w+):(?P<remotePath>(?:(?:\/[A-z._-])\w+)+) (?P<localPath>(?:(?:\/[A-z._-])\w+)+)
        # pattern = re.compile("#(?P<username>[A-z._])\w+@(?P<hostname>[A-z._])\w+:(?P<remotePath>(?:\/[A-z._-])\w+)+ (?P<localPath>(?:\/[A-z._-])\w+)+")
        for key, stringData in dataSection.items():
            print (key)
            print (stringData)
            match = re.match(r"#(?P<username>(?:[A-z 1-9._])\w+)", stringData)
            if(match):
                data[key] = match.group("username")
            else:
                print ("caca")
        return data

    def loadTemplate(self):
        templateDirectory = dirname(abspath(__file__)) + "/Template"
        self.headTemplate = read(templateDirectory + "/head.template")
        self.entryTemplate = read(templateDirectory + "/entry.template")
        self.tailTemplate = read(templateDirectory + "/tail.template")

    def commit(self):
        """
        Save the content of the currentData to the fstab file
        """
        fstabContent = self.rebuildFstab(self.fstab)
        dump(self.fstab.path, fstabContent)

    def makeAutogenSection(self, autogenDict):
        """
        Build the fstab autogen section
        :param autogenDict: The data that the fstab file must contain
        """
        lineFeed = "\n"
        autogenString = self.headTemplate + lineFeed

        for key, value in autogenDict.items():
            autogenString += self.entryTemplate.format(**value)

        autogenString += self.tailTemplate
        return autogenString

    def rebuildFstab(self, fstabEntity):
        """
        Concatenate the 3 strings together
        :param before: a list of every line of the content before the autogen section
        :param autoGen: the string representation of the autogen section
        :param after: a list of every line of the content after the autogen section
        :return: the entire fstab file in a string
        """
        lineFeed = "\n"
        fstab = ""
        autogen = self.makeAutogenSection(fstabEntity.data)

        for line in fstabEntity.pre:
            fstab += line

        fstab += autogen

        for line in fstabEntity.after:
            fstab += line

        return fstab

    def isAutoGenSection(self, line):
        """
        Check if the line is inside the autogen section
        """
        result = False

        if not self.inAutoGen:
            # If the current line equal to the head -> we enter the autogen
            if line == self.headTemplate:
                result = True
        else:
            # If the current line equal to the tail -> we exit the autogen
            if line != self.tailTemplate:
                result = True

        return result

    def compare(self, stringOne, stringTwo):
        """
        Do a character by character comparison
        :param stringOne: the string one
        :param stringTwo: the string two
        """
        result = False

        for i in range(0, len(stringOne)):
            try:
                # Can raise an IndexError too
                if stringOne[i] != stringTwo[i]:
                    raise Exception
            except Exception as e:
                break
        else:
            result = True
        return result
        # ?P<name> is an ID that can be retrieved with the match object
