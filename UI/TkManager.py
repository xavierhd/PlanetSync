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
            self.setClosingOperation(callback)
        self.content = []
        self.asyncResponse = None
        self.lock = Lock()

    def run(self):
        """
        Launch the UI mainloop
        """
        self.tk.mainloop()

    def removeAll(self):
        """
        Delete the all the component from the window
        """
        for item in self.content:
            item.grid_forget()
        self.content = []

    def addSpacer(self):
        """
        Add a spacer in the window
        """
        self.content.append(Label(self.tk, text=" "))
        self.lastContent().grid(row=len(self.content))

    def addLabel(self, text):
        """
        Add a label to the window
        :param text: The text to display on the label
        """
        self.content.append(Label(self.tk, text=text))
        self.lastContent().grid(row=len(self.content))
        return self.lastContent()

    def addEntry(self, isPassword=False):
        """
        Add an entry field
        :param isPassword: True to obfuscate the entry field
        :return: the created entry
        """
        if isPassword:
            self.content.append(Entry(self.tk, show="*"))
        else:
            self.content.append(Entry(self.tk))
        self.lastContent().grid(row=len(self.content))
        return self.lastContent()

    def addListbox(self, actionButtonText=None, callback=None, args=None):
        """
        Add a listbox
        :param actionButtonText: The text to show in the button, if no text is provided, no button is shown
        :param callback: A function executed on button press
        :param args: The argument to give to the callback
        :return: the created listbox
        """
        self.content.append(Listbox(self.tk))
        listbox = self.lastContent()
        listbox.grid(row=len(self.content))
        if actionButtonText:
            self.content.append(Button(self.tk, text=actionButtonText))
            self.lastContent().grid(row=len(self.content)-1, column=1)
        return listbox

    def addButton(self, text, mustReturn=False, callback=None, args=None):
        """
        Add a button to the tkWindow
        :param text: The content of the button
        :param mustReturn: True to destroy the window, False to only return control to the caller
        :param callback: A function executed on button press
        :param args: The argument to give to the callback
        :return: The created button
        """

        # Method to call when clicked
        action = [callback, self.quit if mustReturn else None]
        args = [args, None]
        onClick = self.makeLambda(action, args)

        self.content.append(Button(self.tk, text=text, command=onClick))
        self.lastContent().grid(row=len(self.content), sticky=W, pady=4)
        return self.lastContent()

    ################################
    # Util functions
    ################################
    def setClosingOperation(self, callback):
        # Define what to do when the window close
        self.tk.protocol("WM_DELETE_WINDOW", callback)

    def setWindowTitle(self, title):
        """
        Change the window bar text
        :param title: The text to be set
        """
        self.tk.wm_title(title)

    def lastContent(self):
        """
        :return: The last added content
        """
        return self.content[-1]

    def makeLambda(self, actions, args=None):
        """
        Build a lambda expression
        :param actions: a list of function
        :param args: a list of args to feed each functions call
        """
        return lambda: self.superLambda(actions, args)

    def superLambda(self, actions, args):
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

    def setAsyncResponse(self, args=None):
        """
        Use this to save some function return value and access it later
        """
        self.lock.acquire()
        try:
            self.asyncResponse = args()
        except TypeError:
            # args is definitely not a function
            self.asyncResponse = args
        self.lock.release()

    def getAsyncResponse(self):
        """
        Access the saved response from the set caller previously
        """
        self.lock.acquire()
        val = self.asyncResponse
        self.asyncResponse = None
        self.lock.release()
        return val
