#!/usr/bin/env python3
"""
    PlanetSync
    The SSH Directory Mounter
    Create an ssh file share with your home's dynamic IP server
"""
from pprint import pprint

from UI.GUI import GUI
import Operation


class Commander(object):

    running = None

    def __init__(self):
        self.gUI = GUI(self.callBack, language="english")
        self.run()
        print ("This is the end")

    def run(self):
        """
        Main loop of the program
        """
        self.running = True
        while self.running:
            Operation.MainMenu(self.gUI, self.callBack)

    def callBack(self, args="quit"):
        """
        Function call if some operation need to return control to the basic Launcher
        """
        if args == "quit":
            self.terminate()

    def terminate(self):
        self.running = False
        self.gUI.terminate()

if __name__ == '__main__':
    Commander()
