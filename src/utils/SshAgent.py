import sys
import pexpect
from paramiko.client import SSHClient
from scp import SCPClient

from utils import FileReader


class SshAgent(object):
    client = None
    defautTimeout = 5

    def __init__(self):
        pass

    def testSshfs(self, info):
        client = self.getClient()
        client.load_system_host_keys()
        client.connect(info["hostname"])
        stdin, stdout, stderr = client.exec_command('ls -l')

    def createKey(self, filename="planetSync"):
        # TODO: Check if key exist before trying to create it
        # If a filename is provided, we need to format a bit the string
        if filename:
            filename = "-f "+filename
        try:
            child = pexpect.spawn("ssh-keygen -q {0}".format(filename))
            child.logfile = sys.stdout
            print("child 0: \n", child)
        except Exception as e:
            print (e)

    def addKey(self, info):
        keyPath = "~/.ssh/planetSync.pub"
        if not FileReader.read(keyPath):
            self.createKey(keyPath)
        try:
            command = "ssh-copy-id {username}@{hostname}".format(**info)
            child = pexpect.spawn(command)
            self.defautExpect(child, info)
        except Exception as e:
            import traceback; traceback.print_exc()
            print (e)

    def sshfs(self, info):
        print (info)
        try:
            command = "sshfs {username}@{hostname}:{remotePath} {localPath}".format(**info)
            child = pexpect.spawn(command)
            self.defautExpect(child, info)
        except Exception as e:
            import traceback; traceback.print_exc()
            print (e)

    def defautExpect(self, child, info, otherExpect=None):
        """
        Execute the usual expected ssh answer
        :param child: the pexpect process
        :param info: dictionary with {username, hostname, password} keys
        :param otherExpect: possible expected pexpect output
        :return: ?
        """
        sshExpected = [
            "The authenticity of host.*",
            "{username}@{hostname}'s password: ".format(**info),
            pexpect.EOF
        ]
        result = -1
        try:
            #Useful to log info inside the terminal.
            #TODO: I may use another file to log this
            #child.logfile = sys.stdout
            #print("child 0: \n", child)
            index = child.expect(sshExpected, timeout=self.defautTimeout)
            if index == 0:
                child.sendline("yes")
                index = child.expect(sshExpected, timeout=self.defautTimeout)
            if index == 1:
                child.sendline(info["password"])
                index = child.expect(sshExpected, timeout=self.defautTimeout)
            if index == 2:
                print ("It worked like a charm!")
                result = None
            else:
                result = index
        except Exception as e:
            print (e)
        return result


    #########################
    # Class specific method #
    #########################
    def connectClient(self, info):
        self.getClient().connect(compress=True, **info)

    def getClient(self):
        return self.client if self.client else self.makeClient()

    def makeClient(self):
        self.client = SSHClient()
        return self.client
