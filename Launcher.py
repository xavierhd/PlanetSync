#!/usr/bin/env python3
"""
    PlanetSync
    The SSH Directory Mounter
    Create an ssh file share with your home's dynamic IP server
"""
import requests
from threading import Thread
from pprint import pprint

from UI.GUI import GUI
import Operation
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
        while running:
            Operation.Menu(self.gUI)

    def callBack(self, args):
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
