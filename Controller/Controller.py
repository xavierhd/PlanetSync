"""For now, it is a container"""

class Controller(object):

    windowManager = None
    callBack = None
    sshAgent = None
    fstabHandler = None
    language = "english"  # Default value

    def __init__(self, windowManager=None, sshAgent=None, fstabHandler=None, callBack=None, controller=None):
        if(controller):
            self.windowManager = controller.windowManager
            self.sshAgent = controller.sshAgent
            self.fstabHandler = controller.fstabHandler
            self.callBack = controller.callBack
        else:
            self.windowManager = windowManager
            self.sshAgent = sshAgent
            self.fstabHandler = fstabHandler
            self.callBack = callBack

    def setLanguage(self, language):
        """Change the used language"""
        self.language = language

    def destroy(self):
        """Terminate the main window instance"""
        self.windowManager.destroy()

    """"abstract"""
    def refresh(self):
        """Refresh the main window instance"""
        raise NotImplementedError("abstract method must be overridden")

    """abstract"""
    def run(self):
        """Launch the window mainloop"""
        raise NotImplementedError("abstract method must be overridden")

    """abstract"""
    def callback(self, args):
        """The function called by """
        raise NotImplementedError("abstract method must be overridden")
