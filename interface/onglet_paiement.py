from base_donnees.historique import affichage_paiement
from base_donnees.paiement import save_paiement
from PyQt6.QtWidgets import (
    QWidget, QApplication, QPushButton, QToolBox, QLabel, QVBoxLayout, QStackedWidget, QTableView, QTabWidget,
    QMainWindow, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QMessageBox,QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QStandardItemModel, QStandardItem

import sys

class Onglet_paiement (QWidget):
    def __init__(self):
        super().__init__()
        layout_principal= QHBoxLayout(self)

        self.sous_onglets= QToolBox()
     
        page_save= QWidget()
        page_show= QWidget()
        self.sous_onglets.addItem(page_save,"Enregistrer un paiement")
        self.sous_onglets.addItem(page_show,"Liste des paiements")

        self.stack= QStackedWidget()

        page_enregistrement= QWidget()
        layout_enregistrement= QFormLayout()
        self.id_etudiant= QLineEdit()
        self.id_etudiant.setPlaceholderText("Nombre uniquement")
        self.matricule= QLineEdit()
        self.montant= QDoubleSpinBox()
        self.montant.setMinimum(5)
        self.montant.setMaximum(1000)
        self.montant.setPrefix("$")
        self.montant.setSingleStep(10)
        self.btn_save= QPushButton("Enregistrer")
        self.btn_save.clicked.connect(self.enregistrer)
        layout_enregistrement.addRow("ID ETUDIANT",self.id_etudiant)
        layout_enregistrement.addRow("MATRICULE :",self.matricule)
        layout_enregistrement.addRow("Montant:",self.montant)
        
        layout_enregistrement.addWidget(self.btn_save)

        page_enregistrement.setLayout(layout_enregistrement)
#-----------------------------------------------------------------------------------------------------------------------
# ----------------------------------- PAGE AFFICHER --------------------------------------------------------------------
        page_afficher = QWidget()
        layout_afficher = QVBoxLayout()
        #----------------------------- DEFINITION DU MENU ------------------------------------------------------
        self.menu= QWidget()
        menu = QHBoxLayout()
        self.champ_recherche= QLineEdit()
        self.btn_search= QPushButton("🔍 Rechercher")
        #self.btn_search.clicked.connect(self.rechercher)
        self.filtrer = QComboBox()
        self.filtrer.addItems(["Filtrer...", "Par étudiant","Ancien ➡️ Récent ","Récent ➡️ Ancien "])
        menu.addWidget(self.champ_recherche, 2)
        menu.addWidget(self.btn_search,2)
        menu.addWidget(self.filtrer,1)
        self.menu.setLayout(menu)

        #---------------------------- TABLEAU D'AFFICHAGE -----------------------------------------------------
        self.table= QTableView()

        layout_afficher.addWidget(self.menu)
        layout_afficher.addWidget(self.table)

        page_afficher.setLayout(layout_afficher)

        self.stack.addWidget(page_enregistrement)
        self.stack.addWidget(page_afficher)
        self.sous_onglets.currentChanged.connect(self.controle_onglet)
        layout_principal.addWidget(self.sous_onglets,1)
        layout_principal.addWidget(self.stack,4)
        self.setLayout(layout_principal)
    def controle_onglet(self,index):
        self.stack.setCurrentIndex(index)
        if index== 1:
            self.afficher()
#------------------------------------------------------------------------------------------------------------------------
    def renitialiser(self):
        self.id_etudiant.clear()
        self.montant.clear()
        self.matricule.clear()
#-----------------------------------------------------------------------------------------------------------------------
    def enregistrer(self):
        id_etudiant= self.id_etudiant.text()
        matricule= self.matricule.text()
        montant=self.montant.value()
        message= save_paiement(
            id_etudiant=id_etudiant,
            matricule=matricule.lower(),
            montant=montant

        )
        QMessageBox.information(self,"SUCCES", message)
        self.renitialiser()
#----------------------------------------------------------------------------------------------------------------------
    def afficher(self):
        en_tete= ["ID","Nom","Matricule","ID ETUDIANT","Montant","Date Paiement"]
        requete= affichage_paiement()
        modele= QStandardItemModel(len(requete),len(en_tete))
        modele.setHorizontalHeaderLabels(en_tete)

        for row_index, ligne in enumerate(requete):
            for col_index, valeur in enumerate(ligne):
                item = QStandardItem(str(valeur))
                modele.setItem(row_index,col_index,item)
        self.table.setModel(modele)
        self.table.resizeColumnsToContents()
#-----------------------------------------------------------------------------------------------------------------