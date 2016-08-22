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
        self.setPrimaryList()

    def setPrimaryList(self, serverList):
        self.primaryList.delete(0, END)
        for server in serverList:
            self.primaryList.insert(END, server)