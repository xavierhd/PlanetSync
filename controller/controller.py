"""For now, it is a container"""

class Controller(object):

    windowManager = None
    callBack = None
    sshAgent = None
    fstabHandler = None

    def __init__(self, windowManager=None, sshAgent=None, fstabHandler=None, callBack=None, controller=None):
        """
        This class can be created using two methods:
        1: Provide all arguments, but the last
        2: Provide the last argument
        :param windowManager: The window manager to use
        :param sshAgent: The instance of the SshAgent
        :param fstabHandler: The instance of the FstabHandler
        :param callBack: A function used to give information about the running process
        :param controller: And instance of a Controller or any class extending Controller, used to make a copy of it
        """
        if controller:
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
    def callback(self, arg, **args):
        """
        The function used to be notified by window event
        :param arg: What need to be done
        :param args: information about why the function has been call and to help to dispatch
        """
        raise NotImplementedError("abstract method must be overridden")
