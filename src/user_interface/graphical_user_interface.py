from user_interface.tk_manager import TkManager
from i18n import language_selector


class GUI:
    """
    Tkinter GUI, high level tools
    """

    window_manager = None
    callback = None
    string = None

    def __init__(self, window_manager, callback, language="english"):
        """
        :param window_manager: An instance of TkManager
        :param callback: A function to bind button to
        :param language: The language to use, TODO: Deprecate this
        """
        self.callback = callback
        self.string = language_selector.get_lang(language)
        self.window_manager = window_manager

    def show(self):
        raise NotImplementedError('abstract method must be overridden')

    def info(self, text, tk_manager=None):
        """
        :param text: The text to display
        :param tk_manager: An instance of TkManager. If no manager is given, a info will be displayed as a popup
        """
        tkm = self.get_tk_manager(tk_manager)
        tkm.add_label(text)
        if not tk_manager:
            tkm.add_button("Understood!", must_return=True, callback=tkm.quit())
            tkm.run()

    def get_password(self, text='Enter your password', tk_manager=None):
        """
        Show an obfuscated entrybox to let user input password
        :param text: The text to display as a hint over the password field
        :param tk_manager: An instance of TkManager. If no manager, a popup is used instead
        :return: The password field / Popup: The password input by the user
        """
        tkm = self.get_tk_manager(tk_manager)
        tkm.remove_all()
        tkm.add_label(text)
        entry = tkm.add_entry(isPassword=True)
        tkm.add_button("Continue", must_return=True, callback=tkm.set_async_response, args=entry.get)
        tkm.run()
        return tkm.get_async_response()

    def get_info(self, text, tk_manager=None):
        """
        Show an entrybox to let the user input information
        :param text: The text to display as a hint over the info field
        :param tk_manager: An instance of TkManager. If no manager, a popup is used instead
        :return: The info field / Popup: The info input by the user
        """
        tkm = self.get_tk_manager(tk_manager)
        tkm.remove_all()
        tkm.add_label(text)
        entry = tkm.add_entry()
        tkm.add_button("Continue", must_return=True, callback=tkm.set_aync_response, args=entry.get)
        tkm.run()
        return tkm.get_async_response()

    def get_choices(self, title, choices, tk_manager=None, callback=None, append=None):
        """
        Show a list of button choice to the user
        :param choices: array of choices
        :return: The index of the clicked button
        """
        is_popup = True if tk_manager else False
        tkm = self.get_tk_manager(tk_manager)
        if not append:
            tkm.remove_all()
        if not callback:
            callback = tkm.set_async_response

        tkm.add_label(title)
        for i in range(len(choices)):
            tkm.add_button(choices[i], must_return=is_popup, callback=callback, args=i)
        if not tk_manager:
            tkm.run()
            return tkm.get_async_response()

    def get_tk_manager(self, tk_manager=None):
        """
        Get a tkManager instance. If the param is None, return a new TkManager
        :param tkManager: should contain a tkManager instance.
        :return: a tkManager
        """
        if tk_manager:
            tkm = tk_manager
        else:
            tkm = TkManager()
        return tkm

    def set_closing_operation(self, callback):
        """
        Set the callback for closing operation
        :param callback: A function to call when the window is closed
        """
        self.window_manager.set_closing_operation(callback)

    def run(self):
        """
        Init the window component and run the UI main loop
        """
        self.window_manager.run()

    def terminate(self):
        """
        Put an end to all this crazyness
        """
        self.window_manager.destroy()
