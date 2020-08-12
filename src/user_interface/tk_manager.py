from tkinter import *
from threading import Lock


class TkManager(object):
    """
    Low level tkinter manager
    Create an instance of it,
    Call run to show the window
    You can pass your own callback to buttons,
    but you can also get the clicked button value with getAsyncResponse
    """

    def __init__(self, callback=None):
        self.tk = Tk()
        if callback:
            self.set_closing_operation(callback)
        self.content = []
        self.async_response = None
        self.lock = Lock()

    def run(self):
        """
        Launch the UI mainloop
        """
        self.tk.mainloop()

    def remove_all(self):
        """
        Delete all the component from the window
        """
        for item in self.content:
            item.grid_forget()
        self.content = []

    def add_spacer(self):
        """
        Add a spacer in the window
        """
        spacer = Label(self.tk, text=" ")
        self.add_widget_to_content(spacer)

    def add_label(self, text):
        """
        Add a label to the window
        :param text: The text to display on the label
        """
        label = Label(self.tk, text=text)
        self.add_widget_to_content(label)
        return label

    def add_entry(self, isPassword=False):
        """
        Add an entry field
        :param isPassword: True to obfuscate the entry field
        :return: the created entry
        """
        if isPassword:
            entry = Entry(self.tk, show="*")
        else:
            entry = Entry(self.tk)
        self.add_widget_to_content(entry)
        return entry

    def add_listbox(self, button=None, callback=None, args=None):
        """
        Add a listbox
        :param actionButtonText: The text to show in the button, if no text is provided, no button is shown
        :param callback: A function executed on button press
        :param args: The argument to give to the callback
        :return: the created listbox
        """
        listbox = Listbox(self.tk)
        self.add_widget_to_content(listbox)
        if button:
            button.grid(row=len(self.content)-1, column=1)
            self.content.append(button)
        return listbox

    def add_button(self, text, must_return=False, callback=None, args=None):
        """
        Add a button to the tkWindow
        :param text: The content of the button
        :param must_return: True to destroy the window, False to only return control to the caller
        :param callback: A function executed on button press
        :param args: The argument to give to the callback
        :return: The created button
        """
        # Method to call when clicked
        action = [callback, self.quit if must_return else None]
        args = [args, None]
        on_click = self.make_lambda(action, args)
        button = Button(self.tk, text=text, command=on_click)
        button.grid(row=len(self.content), sticky=W, pady=4)
        self.content.append(button)
        return self.last_content()

    def add_widget_to_content(self, widget):
        widget.grid(row=len(self.content))
        self.content.append(widget)

    ################################
    # Util functions
    ################################
    def set_closing_operation(self, callback):
        # Define what to do when the window close
        self.tk.protocol("WM_DELETE_WINDOW", callback)

    def set_window_title(self, title):
        """
        Change the window bar text
        :param title: The text to be set
        """
        self.tk.wm_title(title)

    def last_content(self):
        """
        :return: The last added content
        """
        return self.content[-1]

    def make_lambda(self, actions, args=None):
        """
        Build a lambda expression
        :param actions: a list of function
        :param args: a list of args to feed each functions call
        """
        return lambda: self.super_lambda(actions, args)

    def super_lambda(self, actions, args):
        """
        Pack any function and it args inside a lambda call
        :param actions: a list of function
        :param args: a list of args to be passed to the function
        """
        for i in range(len(actions)):
            # If the action exist
            if actions[i] is not None:
                # If the action have a corresponding function
                if args is not None \
                        and i < len(args) \
                        and args[i] is not None:
                    actions[i](args[i])
                else:
                    actions[i]()

    def destroy(self):
        """
        Destroy the window instance
        """
        self.tk.destroy()

    def quit(self):
        """
        Stop the main loop
        """
        self.tk.quit()

    def set_async_response(self, args=None):
        """
        Use this to save some function return value and access it later
        """
        self.lock.acquire()
        try:
            self.async_response = args()
        except TypeError:
            # args is definitely not a function
            self.async_response = args
        self.lock.release()

    def get_async_response(self):
        """
        Access the saved response from the set caller previously
        """
        self.lock.acquire()
        val = self.async_response
        self.async_response = None
        self.lock.release()
        return val
