#!/usr/bin/env python3
"""
PlanetSync
The SSH Directory Mounter
Create an ssh file share with your home's dynamic IP server
"""
from pprint import pprint

from controller import Controller
from controller.easy_menu import EasyMenu
from controller.connection_manager import ConnectionManager

from utils.network.ssh_agent  import SshAgent
from utils.fstab import FstabHandler
from ui import TkManager

from locale import lang_selector


class PlanetSync(object):
    """
    The main class which manage the windows controller
    """

    running = None

    def __init__(self):
        self.language = "english"  # TODO: Should be inside some config file
        # The core container
        self.controller = Controller(TkManager(), SshAgent(), FstabHandler(), self.callback)
        lang_selector.setLang(self.language)
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
        current = self.controllerList.pop()
        # current.destroy()
        self.controllerList[-1].run()

    def callback(self, arg="quit"):
        """
        Function call if some operation need to return control to the basic Launcher
        """
        action = {
            'connectionManager': self.startConnectionManager,
            'back': self.launchPrevious,
            'quit': self.terminate,
        }
        try:
            action[arg]()
        except KeyError as e:
            print("This callback command is wrong : {0}, {1}".format(arg, e))

    def terminate(self):
        """
        End the application
        """
        self.controller.destroy()

if __name__ == '__main__':
    PlanetSync()
