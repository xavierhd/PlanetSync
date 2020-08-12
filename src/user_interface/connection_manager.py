from user_interface.tk_manager import TkManager
from user_interface.graphical_user_interface import GUI
from tkinter import Listbox, Button, END


class ConnectionManager(GUI):
    """
    Interface having a clickable list of server.
    Each clicked item show in a second list the associated share.
    A double click/Right click any item open an edition window to change related parameter.
    """

    # Watchout, these are not the UI element, but the content of those
    primary_list = None
    secondary_list = None

    def __init__(self, window_manager, callback, language):
        super().__init__(window_manager, callback, language)

    """Override GUI.show"""
    def show(self):
        """
        Init the window component
        """
        self.window_manager.set_window_title(self.string["connectionManager"]["title"])
        self.window_manager.remove_all()
        self.window_manager.add_label(self.string["connectionManager"]["instruction"])
        self.window_manager.add_spacer()

        self.window_manager.add_label(self.string["connectionManager"]["primaryListTitle"])
        self.primary_list = self.window_manager.add_listbox()
        self.window_manager.add_spacer()

        self.window_manager.add_label(self.string["connectionManager"]["secondaryListTitle"])
        buttonSecondaryList = Button(self.window_manager.tk,
            text=self.string["connectionManager"]["buttonSecondaryList"],
            command=self.window_manager.make_lambda([self.callback], ["addShare"]))
        self.secondary_list = self.window_manager.add_listbox(buttonSecondaryList)
        self.window_manager.add_spacer()
        self.window_manager.add_button(self.string["general"]["buttonBack"], callback=self.callback, args="back")

    def add_to_list(self, target_listbox, newItem):
        target_listbox.insert(END, newItem)

    def set_list(self, target_listbox, serverList):
        """
        Set the provided list with the content of the provided serverList
        :param target_listbox: The listbox instance to be setted
        :param serverList: An array of new values
        """
        target_listbox.delete(0, END)
        for server in serverList:
            target_listbox.insert(END, server)

    def show_advanced(self):
        tkm = TkManager()
        tkm.add_label(self.string["advanced"]["title"])
        tkm.add_label(self.string["advanced"]["info"])
        for entry in self.string["advanced"]["choices"]:
            pass

    def get_ssh_info(self):
        return {
            "hostname": self.get_info(self.string["question"]["get"]["remote_ip"],
                                     tk_manager=self.window_manager),
            "username": self.get_info(self.string["question"]["get"]["remote_user"],
                                     tk_manager=self.window_manager),
            "password": self.get_password(self.string["question"]["get"]["remote_pw"],
                                         tk_manager=self.window_manager)
        }

    def sshfs_info_window(self, entry=None):
        tkm = self.get_tk_manager(None)
        # tkm.addTitle("SSH connection entry")
        tkm.add_label("Please provide your remote computer's information: ")
        tkm.add_label(self.string["question"]["get"]["remote_ip"])
        entryHostname = tkm.add_entry()
        tkm.add_label(self.string["question"]["get"]["remote_user"])
        entryUsername = tkm.add_entry()
        tkm.add_label(self.string["question"]["get"]["remote_pw"])
        entryPassword = tkm.add_entry(True)
        if entry:
            entryHostname.set(entry["hostname"])
            entryUsername.set(entry["username"])
            entryPassword.set(entry["password"])

        tkm.add_button("Continue", must_return=False)
        tkm.run()
        return {
            "hostname": entryHostname.get(),
            "username": entryUsername.get(),
            "password": entryPassword.get(),
        }

    def mount_info_window(self, entry=None):
        tkm = self.get_tk_manager(None)
        # tkm.addTitle("SSH connection entry")
        tkm.add_label(self.string["question"]["get"]["remote_path"])
        entry_remote_path = tkm.add_entry()
        tkm.add_label(self.string["question"]["get"]["local_path"])
        entry_local_path = tkm.add_entry()
        if entry:
            entry_remote_path.set(entry["remote_path"])
            entry_local_path.set(entry["local_path"])

        tkm.add_button("Continue", must_return=False)
        tkm.run()
        return {
            "hostname": entry_remote_path.get(),
            "username": entry_local_path.get(),
        }
