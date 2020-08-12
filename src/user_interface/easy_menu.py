from user_interface.graphical_user_interface import GUI

class EasyMenu(GUI):
    """
    Easy to use interface for beginner
    """

    def __init__(self, window_manager, callback, language):
        super().__init__(window_manager, callback, language)

    """Override GUI.show"""
    def show(self):
        """
        Init the menu UI component
        """
        self.window_manager.set_window_title(self.string["menu"]["title"])
        self.window_manager.remove_all()
        self.window_manager.add_label(self.string["menu"]["info"])
        self.get_choices(self.string["menu"]["operation"],
                            self.string["menu"]["choice"],
                            tk_manager=self.window_manager,
                            callback=self.callback,
                            append=True)

    def get_ssh_info(self):
        """
        Show multiple popup window just like an install wizard,
        asking for mandatory information to make an ssh connection
        """
        return {
            "hostname": self.get_info(self.string["question"]["get"]["remote_ip"],
                                     tk_manager=self.window_manager),
            "username": self.get_info(self.string["question"]["get"]["remote_user"],
                                     tk_manager=self.window_manager),
            "password": self.get_password(self.string["question"]["get"]["remote_pw"],
                                         tk_manager=self.window_manager)
        }

    def get_sshfs_info(self):
        """
        Show multiple popup windows just like an install wizard,
        asking for mandatory information to make an sshfs connection
        """
        info = self.get_ssh_info()
        info["remotePath"] = self.get_info(self.string["question"]["get"]["remote_path"],
                                          tk_manager=self.window_manager)
        info["localPath"] = self.get_info(self.string["question"]["get"]["local_path"],
                                         tk_manager=self.window_manager)
        return info
