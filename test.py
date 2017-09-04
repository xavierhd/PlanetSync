#!/usr/bin/env python3

from unittest.mock import MagicMock

from utils.ssh_agent import SshAgent
from utils import FileReader


def main():
    ssh = SshAgent()
    ssh.sshfs(FileReader.readYaml("/home/xavier/Projet/testFile.yaml"))

def testSshAgent():
    ssh = SshAgent()
    ssh.test()

if __name__ == '__main__':
    testSshAgent()
