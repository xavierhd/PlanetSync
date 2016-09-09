"""
Interface ayant une liste sélectionnable de serveur.
Chaque item cliqué affiche la liste des partages associés dans une liste secondaire.
Un "Double clique?"/"Bouton à droite" sur un item de l'inteface permet de modifier ces informations.
"""

from Controller import Controller
from UI.ConnectionManager import ConnectionManager as UI_ConnectionManager

class ConnectionManager(Controller):


    primaryList = None
    secondaryList = None

    def __init__(self, controller):
        super().__init__(controller=controller)
        self.gUI = UI_ConnectionManager(self.windowManager, self.callback, self.language)

    def run(self):
        self.gUI.setClosingOperation(self.callBack)
        self.gUI.show()
        self.setListBox(self.gUI.primaryList, self.fstabHandler.get())
        self.gUI.run()

    def setListBox(self, listBox, serverList):

        self.gUI.setList(listBox, serverList)

    def addToList(self, listBox, newItem):
        pass

    def callback(self, args):
        """
        Override the extended class
        :param args:
        :return:
        """
        if args == "back":
            self.callBack("back")
        if args is self.primaryList:
            self.setListBox(self.gUI.secondaryList, args)
        elif args is self.secondaryList:
            self.setListBox(self.gUI.primaryList, args)
