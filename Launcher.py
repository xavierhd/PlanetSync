#!/usr/bin/env python3
"""
    PlanetSync
    The SSH Directory Mounter
    Create an ssh file share with your home's dynamic IP server
"""
from pprint import pprint

from Operation.EasyMenu import EasyMenu
from Operation.ConnectionManager import ConnectionManager

from Utils import SshAgent
from Utils.fstab import FstabHandler
from UI import TkManager


class PlanetSync(object):

    running = None

    def __init__(self):
        self.language = "english"  # Should be inside some config file
        self.sshAgent = SshAgent()
        self.fstabHandler = FstabHandler()
        self.windowManager = TkManager()
        self.operation = None
        self.run()
        print ("This is the end")

    def run(self):
        """
        Main loop of the program, was a loop -_-
        """
        self.operation = EasyMenu(self.windowManager,
                                  self.sshAgent,
                                  self.fstabHandler,
                                  self.callBack,
                                  self.language)
        self.operation.run()

    def callBack(self, args="quit"):
        """
        Function call if some operation need to return control to the basic Launcher
        """
        if args == "quit":
            self.terminate()
        elif args == "connectionManager":
            self.operation = ConnectionManager(self.windowManager,
                                               self.sshAgent,
                                               self.fstabHandler,
                                               self.callBack,
                                               self.language)
            self.operation.run()

    def terminate(self):
        self.operation.destroy()

if __name__ == '__main__':
    PlanetSync()
