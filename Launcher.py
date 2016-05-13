#!/usr/bin/env python3
"""
    PlanetSync
    The SSH Directory Mounter
    Create an ssh file share with your home's dynamic IP server
"""
import requests
from threading import Thread

from UI.GUI import GUI
from Utils.SshAgent import SshAgent


class Commander(object):
    cmd = {
        "mount": "sshfs {remoteUser}@{remoteIP}:{remotePath} {localPath}",
        "unmount":"fusermount -u {localPath}",
        "push to server": "scp {localFilePath} {remoteUser}@{remoteIP}:{remoteFilePath}",
        "add to file": "cat {remoteFilePath} >> /home/{remoteUser}/.ssh/authorized_keys",
        "add self to cron": "(crontab -l ; echo '00 09 * * 1-5 runUpdateScript') | crontab -",
        "remoteCommand": "ssh -t {remoteIP} '{command}'"
    }

    def __init__(self):
        self.sshAgent = SshAgent()
        self.gUI = GUI(self.callBack, language="english")
        self.run()
        print ("This is the end")

    def run(self):
        running = True
        runfor = 0
        while running:
            self.gUI.showMenu()
            from pprint import pprint
            pprint (self.gUI.string)
            choice = self.gUI.getChoices(self.gUI.string["menu"]["operation"],
                                         self.gUI.string["menu"]["choice"],
                                         tkManager=self.gUI.mainWindow)
            if choice == 0:
                info = self.gUI.getSshfsInfo()
                self.sshAgent.sshfs(info)
            elif choice == 1:
                info = self.gUI.getSshInfo()
                self.sshAgent.addKey(info)

    def callBack(self, args):
        pass

    def command(self, command, args):
        process = subprocess.Popen(command.format(**args).split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        #This is the return value of the command
        if "belzebuth@192.168.0.2's password: " in process.communicate():
            print ("bravo")
        else:
            print ("pas bravo")
        return ''.join([p for p in process.communicate() if p])

    def icommand(self, command, args):
        pass

    def internetExist(self):
        r = requests.head("http://google.ca")
        return str(r.status_code) == '301'



    def readIP(self, path):
        ip = None
        try:
            with open(path) as file:
                ip = f.readline()
        except:
            print ("no file named %s" %path)
        return ip

if __name__ == '__main__':
    Commander()
