import subprocess

from paramiko.client import SSHClient
from scp import SCPClient


class SshAgent(object):
	client = None

	def makeClient(self):
		self.client = SSHClient()