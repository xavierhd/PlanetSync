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

    """Override Controller.run"""
    def run(self):
        self.gUI.run()

    def setListBox(self, listBox, serverList):
        """
        Set the content of a listbox
        :param listBox: The listBox to be modified
        :param serverList: An array of server to be displayed in the listBox
        """
        self.gUI.setList(listBox, serverList)

    def addToList(self, listBox, newItem):
        """
        Add one item to the provided listBox
        :param listBox: The listbox to be modified
        :param newItem: The element to add to the listbox
        """
        listBox.insert(END, newItem)

    """Override Controller.callback"""
    def callback(self, args):
        if args == "back":
            self.callBack()
        if args is self.primaryList:
            self.setListBox(self.gUI.secondaryList, args)
        elif args is self.secondaryList:
            self.setListBox(self.gUI.primaryList, args)
