import subprocess
import sys

import pexpect
from paramiko.client import SSHClient
from scp import SCPClient


class SshAgent(object):
    client = None


    def __init__(self):
        pass


    def addKey(self, info):
        self.getClient().connect(compress=True, **info)

    def sshfs(self, info):
        print (info)
        expected = [
            "The authenticity of host.*",
            "{username}@{hostname}'s password: ".format(**info),
            pexpect.EOF
                   ]
        try:
            child = pexpect.spawn("sshfs {username}@{hostname}:{remotePath} {localPath}".format(**info))
            #Useful to log info inside the terminal.
            #TODO: I may use another file to log this
            #child.logfile = sys.stdout
            print("child 0: \n", child)
            index = child.expect(expected, timeout=5)
            print("child 1 {0}: \n".format(index), child)
            if index == 0:
                child.sendline("yes")
                print("child 2: \n", child)
                index = child.expect(expected, timeout=5)
                print("child 3: \n", child)
            if index == 1:
                child.sendline(info["password"])
            if index == 2:
                print ("we are")

        except Exception as e:
            import traceback; traceback.print_exc()
            print (e)

    #########################
    # Class specific method #
    #########################
    def getClient(self):
        return self.client if self.client else makeClient()

    def makeClient(self):
        self.client = SSHClient()
        return self.client
