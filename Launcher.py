#!/usr/bin/env python3
"""
    PlanetSync
    The SSH Directory Mounter
    Create an ssh file share with your home's dynamic IP server
"""
from pprint import pprint

from Controller import Controller
from Controller.EasyMenu import EasyMenu
from Controller.ConnectionManager import ConnectionManager

from Utils import SshAgent
from Utils.fstab import FstabHandler
from UI import TkManager


class PlanetSync(object):

    running = None

    def __init__(self):
        self.language = "english"  # Should be inside some config file
        self.controller = Controller(TkManager(), SshAgent(), FstabHandler(), self.callback)
        self.controller.setLanguage(self.language)
        self.controllerList = []
        self.run()
        print ("This is the end")

    def run(self):
        """
        Main loop of the program, was a loop -_-
        """
        self.startEasyMenu()

    def startEasyMenu(self):
        self.controllerList.append(EasyMenu(self.controller))
        self.controllerList[-1].run()

    def startConnectionManager(self):
        self.controllerList.append(ConnectionManager(self.controller))
        self.controllerList[-1].run()

    def launchPrevious(self):
        self.controllerList.pop()
        self.controllerList[-1].run()

    def callback(self, args="quit"):
        """
        Function call if some operation need to return control to the basic Launcher
        """
        if args == "quit":
            self.terminate()
        elif args == "connectionManager":
            self.startConnectionManager()
        elif args == "back":
            self.launchPrevious()

    def terminate(self):
        self.controller.destroy()

if __name__ == '__main__':
    PlanetSync()
