#!/usr/bin/env python3

from unittest.mock import MagicMock

from UI.LangSelector import getLang
from Utils.SshAgent import SshAgent
from Utils import FileReader


def main():
    ssh = SshAgent()
    ssh.sshfs(FileReader.readYaml("/home/xavier/Projet/testFile.yaml"))

if __name__ == '__main__':
    main()