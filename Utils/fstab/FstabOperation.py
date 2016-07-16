from os.path import expanduser, dirname, abspath
import re # regex utility

from Utils.FileReader import read, readLine, dump

import FstabEntity


class Operation(object):
    """
    Low level interface with the fstab file
    """

    fstab = None

    inAutoGen = False
    FSTAB_FILE = expanduser("~")+"/test_fstab"

    # Fstab file sections
    preAutogen = []
    currentData = {}
    afterAutogen = []

    # Template of the autogenerated section
    headTemplate = None
    entryTemplate = None
    tailTemplate = None

    def __init__(self):
        self.loadTemplate()
        self.fstab = FstabEntity()


    def getKey(self, line):
        key = None
        regex = "##"
        if line:
            split = re.split(regex, line)
            print(split)
            if len(split) >= 2:
                key = split[1]
        return key

    def parseSections(self):
        """
        Parse the fstab into 3 sections: preAutogen, autogen and afterAutogen
        :return: the autogenerated section of the fstab file
        """
        autogenSection = {}
        fstab = readLine(self.FSTAB_FILE)
        key = None
        # If read had returned something
        if fstab:
            for line in fstab:

                # If we are inside the autogen section and the line isn't empty
                if line and self.isAutoGenSection(line):
                    # Make sure that the first run doesn't try to find a key in headTemplate
                    if self.inAutoGen:
                        if not key:
                            key = self.getKey(line)
                        else:
                            autogenSection[key] = line
                            key = None
                    else:
                        self.inAutoGen = True

                # If we are outside and before of autogen section
                elif not self.inAutoGen and not autogenSection:
                    self.preAutogen.append(line)

                # If we are outside and after of autogen section
                elif not self.inAutoGen and autogenSection:
                    self.afterAutogen.append(line)
        return autogenSection

    def loadTemplate(self):
        templateDirectory = dirname(abspath(__file__)) + "/Template"
        self.headTemplate = read(templateDirectory + "/head.template")
        self.entryTemplate = read(templateDirectory + "/entry.template")
        self.tailTemplate = read(templateDirectory + "/tail.template")

    def commit(self):
        """
        Save the content of the currentData to the fstab file
        """
        autogen = self.makeAutogenSection(self.currentData)
        fstabContent = self.rebuildFstab(self.preAutogen, autogen, self.afterAutogen)
        dump(self.FSTAB_FILE, fstabContent)

    def makeAutogenSection(self, autogenDict):
        """
        Build the fstab autogen section
        :param autogenDict: The data that the fstab file must contain
        """
        lineFeed = "\n"
        autogenString = self.headTemplate + lineFeed

        for key, value in autogenDict.items():
            autogenString += self.entryTemplate.format(**value) + lineFeed

        autogenString += self.tailTemplate + lineFeed
        return autogenString

    def rebuildFstab(self, before, autogen, after):
        """
        Concatenate the 3 strings together
        :param before: a list of every line of the content before the autogen section
        :param autoGen: the string representation of the autogen section
        :param after: a list of every line of the content after the autogen section
        :return: the entire fstab file in a string
        """
        lineFeed = "\n"
        fstab = ""
        for line in before:
            fstab += line

        fstab += lineFeed
        fstab += autogen

        for line in after:
            fstab += line

        return fstab

    def isAutoGenSection(self, line):
        """
        Check if the line is inside the autogen section
        """
        result = False

        if not self.inAutoGen:
            # If the current line equal to the head -> we enter the autogen
            if line == self.headTemplate + "\n":
                result = True
        else:
            # If the current line equal to the tail -> we exit the autogen
            if self.compare(line, self.tailTemplate + "\n"):
                self.inAutoGen = False
            else:
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
                # Can raise an IndexError
                if stringOne[i] != stringTwo[i]:
                    raise Exception
            except Exception as e:
                break
        else:
            result = True
        return result
