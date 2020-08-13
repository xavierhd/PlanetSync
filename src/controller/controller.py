"""For now, it is a container"""

class Controller(object):

    parent_callback = None
    sshAgent = None
    fstabHandler = None
    language = "english"  # Default value

    def __init__(self, sshAgent=None, fstabHandler=None, parent_callback=None, controller=None):
        """
        This class can be instanciated using two methods:
        1: Provide all arguments, but the last
        2: Provide only the last argument
        :param window_manager: The window manager to use
        :param sshAgent: The instance of the SshAgent
        :param fstabHandler: The instance of the FstabHandler
        :param parent_callback: A function to be used to give information about the running process
        :param controller: And instance of a Controller of any class extending Controller, used to make a copy of the already built Controller
        """
        if(controller):
            self.sshAgent = controller.sshAgent
            self.fstabHandler = controller.fstabHandler
            self.parent_callback = controller.parent_callback
        else:
            self.sshAgent = sshAgent
            self.fstabHandler = fstabHandler
            self.parent_callback = parent_callback

    def setLanguage(self, language):
        """Change the used language"""
        self.language = language
