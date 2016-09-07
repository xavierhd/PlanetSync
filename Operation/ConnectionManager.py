"""
Interface ayant une liste sélectionnable de serveur.
Chaque item cliqué affiche la liste des partages associés dans une liste secondaire.
Un "Double clique?"/"Bouton à droite" sur un item de l'inteface permet de modifier ces informations.
"""

from Operation import Operation
from UI.ConnectionManager import ConnectionManager as UI_ConnectionManager

class ConnectionManager(Operation):


    primaryList = None
    secondaryList = None

    def __init__(self, windowManager, sshAgent, fstabHandler, callback, language):
        super().__init__(callback, sshAgent, fstabHandler)
        self.gUI = UI_ConnectionManager(windowManager, callback, language)

    def run(self):
        self.gUI.run()

    def setListBox(self, listBox, serverList):
        listBox.delete(0, END)
        for server in serverList:
            listBox.insert(END, server)

    def addToList(self, listBox, newItem):
        listBox.insert(END, newItem)

    def callback(self, caller):
        if caller is self.primaryList:
            self.setListBox(self.secondaryList, info)
        elif caller is self.secondaryList:
            self.setListBox(self.primaryList, info)

    def destroy(self):
        self.gUI.terminate()
