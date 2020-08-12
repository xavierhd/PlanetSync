"""For now, it is a container"""

class Controller(object):

    window_manager = None
    parent_callback = None
    sshAgent = None
    fstabHandler = None
    language = "english"  # Default value

    def __init__(self, window_manager=None, sshAgent=None, fstabHandler=None, parent_callback=None, controller=None):
        """
        This class can be instanciated using two methods:
        1: Provide all arguments, but the last
        2: Provide the last argument
        :param window_manager: The window manager to use
        :param sshAgent: The instance of the SshAgent
        :param fstabHandler: The instance of the FstabHandler
        :param parent_callback: A function to be used to give information about the running process
        :param controller: And instance of a Controller of any class extending Controller, used to make a copy of the already built Controller
        """
        if(controller):
            self.window_manager = controller.window_manager
            self.sshAgent = controller.sshAgent
            self.fstabHandler = controller.fstabHandler
            self.parent_callback = controller.parent_callback
        else:
            self.window_manager = window_manager
            self.sshAgent = sshAgent
            self.fstabHandler = fstabHandler
            self.parent_callback = parent_callback

    def setLanguage(self, language):
        """Change the used language"""
        self.language = language

    def destroy(self):
        """Terminate the main window instance"""
        self.window_manager.destroy()

    """abstract"""
    def run(self):
        """Launch the window mainloop"""
        raise NotImplementedError("abstract method must be overridden")

    """abstract"""
    def callback(self, args):
        """
        The function used to be notified by window event
        :param args: information about why the function has been call and to help to dispatch
        """
        raise NotImplementedError("abstract method must be overridden")
