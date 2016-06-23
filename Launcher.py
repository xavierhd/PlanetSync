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

    cmd = {
        "mount": "sshfs {remoteUser}@{remoteIP}:{remotePath} {localPath}",
        "unmount":"fusermount -u {localPath}",
        "push to server": "scp {localFilePath} {remoteUser}@{remoteIP}:{remoteFilePath}",
        "add to file": "cat {remoteFilePath} >> /home/{remoteUser}/.ssh/authorized_keys",
        "add self to cron": "(crontab -l ; echo '00 09 * * 1-5 runUpdateScript') | crontab -",
        "remoteCommand": "ssh -t {remoteIP} '{command}'"
    }

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

    def callBack(self, args):
        """
        Function call if some operation need to return control to the basic Launcher
        """
        if args == "quit":
            self.running = False

if __name__ == '__main__':
    Commander()
