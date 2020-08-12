
from user_interface.graphical_user_interface import GUI
from user_interface import TkManager

class InfoQuery(GUI):

    is_alive = True

    def __init__(self, language):
        super().__init__(TkManager(), None, language)
        self.set_closing_operation(self.quit)

    def get_share_info(self):
        self.window_manager.add_label(self.string["question"]["get"]["share_name"])
        sharename = self.window_manager.add_entry()

        self.window_manager.add_label(self.string["question"]["get"]["remote_ip"])
        hostname = self.window_manager.add_entry()

        self.window_manager.add_label(self.string["question"]["get"]["remote_user"])
        username = self.window_manager.add_entry()

        self.window_manager.add_label(self.string["question"]["get"]["remote_pw"])
        password = self.window_manager.add_entry(isPassword=True)

        self.window_manager.add_label(self.string["question"]["get"]["remote_path"])
        remote_path = self.window_manager.add_entry()

        self.window_manager.add_label(self.string["question"]["get"]["local_path"])
        local_path = self.window_manager.add_entry()
        self.window_manager.add_spacer()
        self.window_manager.add_button(self.string["general"]["buttonAdd"], must_return=True)
        self.run()
        info = None
        if self.is_alive:
            info =  {
                "shareName": sharename.get(),
                "hostname": hostname.get(),
                "username": username.get(),
                "password": password.get(),
                "remotePath": remote_path.get(),
                "localPath": local_path.get(),
            }
            # Make sure that this tkManager is dead
            self.terminate()
        return info


    def quit(self):
        self.is_alive = False
        self.terminate()
