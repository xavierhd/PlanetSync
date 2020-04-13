#!/usr/bin/env python3

from unittest.mock import MagicMock

#from UI.LangSelector import getLang
from utils.SshAgent import SshAgent
from utils import FileReader


def main():
    ssh = SshAgent()
    ssh.sshfs(FileReader.readYaml("/home/xavier/Projet/.test_file.yaml"))

if __name__ == '__main__':
    main()