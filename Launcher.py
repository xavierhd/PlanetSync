#!/usr/bin/env python3
"""
    PlanetSync
    The SSH Directory Mounter
    Create an ssh file share with your home's dynamic IP server
"""
from pprint import pprint

from UI.EasyMenu import EasyMenu
import Operation

from Operation.ConnectionManager import ConnectionManager
from Utils.fstab.FstabHandler import Handler as FsHandler


class PlanetSync(object):

    running = None

    def __init__(self):
        self.gUI = EasyMenu(self.callBack, language="english")
        self.fstabHandler = FsHandler()
        self.run()
        print ("This is the end")

    def run(self):
        """
        Main loop of the program
        """
        self.running = True
        while self.running:
            Operation.EasyMenu(self.fstabHandler, self.gUI, self.callBack)

    def callBack(self, args="quit"):
        """
        Function call if some operation need to return control to the basic Launcher
        """
        if args == "quit":
            self.terminate()
        if args == "connectionManager":
            ConnectionManager(self.fstabHandler)

    def terminate(self):
        self.running = False
        self.gUI.terminate()

if __name__ == '__main__':
    PlanetSync()
