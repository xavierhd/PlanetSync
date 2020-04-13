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

from utils import SshAgent
from fstab import FstabFile
from user_interface import TkManager


class PlanetSync(object):
    """
    The main class which manage the windows controller
    """

    running = None

    def __init__(self):
        self.language = "english"  # TODO: Should be inside some config file
        path = 'Some_path'
        self.base_controller = Controller(TkManager(), SshAgent(), FstabFile(path), self.callback)
        self.base_controller.setLanguage(self.language)
        # This list contain all the class extending Controller
        self.controllers = []
        self.run()
        print ("This is the end")

    def run(self):
        """
        Main loop of the program, was a loop -_-
        """
        self.controllers.append(EasyMenu(self.base_controller))
        self.controllers[-1].run()

    def start_connection_manager(self):
        self.controllers.append(ConnectionManager(self.base_controller))
        self.controllers[-1].run()

    def launch_previous(self):
        """
        Re-Launch the previously running controller
        """
        current = self.controllers.pop()
        current.destroy()
        self.controllers[-1].run()

    def callback(self, args="quit"):
        """
        Function call if some operation need to return control to the basic Launcher
        """
        if args == "quit":
            self.terminate()
        # Tell the program that the connectionManager need to be launched
        elif args == "connectionManager":
            self.start_connection_manager()
        # Tell the program that the current window has finish it operation.
        # The previous window is shown
        elif args == "back":
            self.launch_previous()

    def terminate(self):
        """
        End the application
        """
        self.base_controller.destroy()

if __name__ == '__main__':
    PlanetSync()
