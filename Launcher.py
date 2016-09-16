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
    """
    The main class which manage the windows controller
    """

    running = None

    def __init__(self):
        self.language = "english"  # TODO: Should be inside some config file
        # The core container
        self.controller = Controller(TkManager(), SshAgent(), FstabHandler(), self.callback)
        self.controller.setLanguage(self.language)
        # This list contain all the class extending Controller
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
        """
        Re-Launch the previously running controller
        """
        self.controllerList.pop()
        self.controllerList[-1].run()

    def callback(self, args="quit"):
        """
        Function call if some operation need to return control to the basic Launcher
        """
        if args == "quit":
            self.terminate()
        # Tell the program that the connectionManager need to be launched
        elif args == "connectionManager":
            self.startConnectionManager()
        # Tell the program that the current window has finish it operation.
        # The previous window is shown
        elif args == "back":
            self.launchPrevious()

    def terminate(self):
        """
        End the application
        """
        self.controller.destroy()

if __name__ == '__main__':
    PlanetSync()
