#!/usr/bin/env python3
"""
    PlanetSync
    The SSH Directory Mounter
    Create an ssh file share with your home's dynamic IP server
"""
import requests
import subprocess
from threading import Thread

from Utils.GUI import GUI


class Commander(object):
    cmd = {
        "mount": "sshfs {remoteUser}@{remoteIP}:{remotePath} {localPath}",
        "unmount":"fusermount -u {localPath}",
        "push to server": "scp {localFilePath} {remoteUser}@{remoteIP}:{remoteFilePath}",
        "add to file": "cat {remoteFilePath} >> /home/{remoteUser}/.ssh/authorized_keys",
        "add self to cron": "(crontab -l ; echo '00 09 * * 1-5 runUpdateScript') | crontab -",
        "remoteCommand": "ssh -t {remoteIP} '{command}'"
    }
    menu = {
        "primary": {
            "title": "PlanetSync",
            "info": "The SSH Directory Mounter\nCreate an ssh file share with your home's dynamic IP server",
            "operation": "What do you want to do ?",
            "choice":[
                "Temporarly mount a folder",
                "Mount a folder forever",
                "Unmount a folder",
                "Remove a folder mounted forever",
            ],
        },
        "question":{
            "confirm": "Are you sure that this is what you want to do?",
            "get": {
                "remote_user": "What is the remote user name?",
                "remote_ip": "What is the remote ip?",
                "remote_dir": "What is the remote directory path?",
                "remote_pw": "What is the remote user password?",

                "mount_dir": "What is the local mounting directory path? (it must be empty)",
            }
        }
    }

    def __init__(self):
        self.gUI = GUI(self.menu["primary"]["title"], self.callBack)
        self.gUI.info(self.menu["primary"]["info"],
                      tkManager=self.gUI.mainWindow,
                      isPopup=False)
        #thread = Thread
        self.run()

    def run(self):
        running = True
        runfor = 0
        while running:
            choice = self.gUI.getChoices(self.menu["primary"]["operation"],
                                         self.menu["primary"]["choice"],
                                         tkManager=self.gUI.mainWindow,
                                         isPopup=False)

            self.gUI.info(choice)
            if runfor == 0:
                running = False
            else:
                runfor = runfor - 1

    def callBack(self, args):
        pass


    def command(self, command, args):
        process = subprocess.Popen(command.format(**args).split(' '), stdout=subprocess.PIPE)
        #This is the return value of the command
        return ''.join([p for p in process.communicate() if p])

    def internetExist(self):
        r = requests.get('https://google.ca')
        return str(r.status_code) == '200'



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
