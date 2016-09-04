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
            # Define what to do on window close
            self.tk.protocol("WM_DELETE_WINDOW", callback)
        self.content = []
        self.asyncResponse = None
        self.lock = Lock()

    def run(self):
        self.tk.mainloop()

    def removeAll(self):
        for item in self.content:
            item.grid_forget()
        self.content = []

    def addLabel(self, text):
        self.content.append(Label(self.tk, text=text))
        self.lastContent().grid(row=len(self.content))
        return self.lastContent()

    def addEntry(self, isPassword=False):
        if isPassword:
            self.content.append(Entry(self.tk, show="*"))
        else:
            self.content.append(Entry(self.tk))
        self.lastContent().grid(row=len(self.content))
        return self.lastContent()

    def addListBox(self, actionButtonText=None, callback=None, args=None):
        self.content.append(ListBox(self.tk))
        self.lastContent().grid(row=len(self.content))
        return self.lastContent()

    def addButton(self, text, mustReturn=False, callback=None, args=None):
        """
        Add a button to the tkWindow
        :param text: The content of the button
        :param mustReturn: True to destroy the window, False to only return control to the caller
        :param callback: A function executed on button press
        :param args: The argument to give to the callback
        :return: The button instance
        """
        action = [callback, self.destroy if mustReturn else self.quit]
        args = [args, None]
        onClick = self.makeLambda(action, args)
        self.content.append(Button(self.tk, text=text, command=onClick))
        self.lastContent().grid(row=len(self.content), sticky=W, pady=4)
        return self.lastContent()

    ################################
    # Util functions
    ################################
    def lastContent(self):
        return self.content[len(self.content) - 1]

    def makeLambda(self, actions, args=None):
        """
        Build a lambda expression
        :param actions: function list
        :param args: actions' args list
        """
        return lambda: self.superLambda(actions, args)

    def superLambda(self, actions, args):
        """
        Pack any function inside a lambda call
        :param actions: a list of function
        :param args: a list of args to be passed to the function
        """
        for i in range(len(actions)):
            if actions[i] is not None:
                if args is not None \
                        and i < len(args) \
                        and args[i] is not None:
                    actions[i](args[i])
                else:
                    actions[i]()

    def destroy(self):
        self.tk.destroy()

    def quit(self):
        self.tk.quit()

    def setAsyncResponse(self, args=None):
        self.lock.acquire()
        try:
            self.asyncResponse = args()
        except TypeError:
            #args is definitely not a function
            self.asyncResponse = args
        self.lock.release()

    def getAsyncResponse(self):
        self.lock.acquire()
        val = self.asyncResponse
        self.asyncResponse = None
        self.lock.release()
        return val
