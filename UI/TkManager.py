from tkinter import *
from threading import Lock

class TkManager(object):
    def __init__(self):
        self.tk = Tk()
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
        if(isPassword):
            self.content.append(Entry(self.tk, show="*"))
        else:
            self.content.append(Entry(self.tk))
        self.lastContent().grid(row=len(self.content))
        return self.lastContent()

    def addButton(self, text, mustReturn=False, callback=None, args=None):
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
        """ Build a lambda expression
            actions: function list
            args: actions' args list"""
        return lambda: self.superLambda(actions, args)

    def superLambda(self, actions, args):
        """ Pack any function inside a lambda call
        """
        for i in range(len(actions)):
            if actions[i] is not None:
                if args is not None and i < len(args) and args[i] is not None:
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
