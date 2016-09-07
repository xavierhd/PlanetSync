"""For now, it is a container"""

class Operation(object):

    callBack = None
    sshAgent = None
    fstabHandler = None

    def __init__(self, callBack, sshAgent, fstabHandler):
        self.callBack = callBack
        self.sshAgent = sshAgent
        self.fstabHandler = fstabHandler

