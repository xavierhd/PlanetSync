"""
Interface ayant une liste sélectionnable de serveur.
Chaque item cliqué affiche la liste des partages associés dans une liste secondaire.
Un "Double clique?"/"Bouton à droite" sur un item de l'inteface permet de modifier ces informations.
"""

from tkinter import Listbox, END

class Wip:

    tkm = None
    primaryList = Listbox()
    secondaryList = Listbox()

    def __init__(self, tkm):
        self.tkm = tkm
        self.tkm.removeAll()
        primaryList = self.tkm.addListBox()
        secondaryList = self.tkm.addListBox()

    def setListBox(self, listBox, serverList):
        listBox.delete(0, END)
        for server in serverList:
            listBox.insert(END, server)

    def addToList(self, listBox, newItem):
        listBox.insert(END, newItem)

    def callback(self, caller, args):
        if caller is self.primaryList:
            self.setListBox(self.secondaryList, info)
        elif caller is self.secondaryList:
            self.setListBox(self.primaryList, info)
