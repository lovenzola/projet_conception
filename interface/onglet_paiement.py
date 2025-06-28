from interface.fonctions_secon import rechercher_proxy
from base_donnees.historique import supprimer_paiement
from base_donnees.paiement import etudiant_existe
from base_donnees.historique import affichage_paiement
from base_donnees.paiement import save_paiement
from PyQt6.QtWidgets import (
    QWidget, QApplication, QPushButton, QToolBox, QLabel, QVBoxLayout, QStackedWidget, QTableView, QTabWidget,
    QMainWindow, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QMessageBox,QDoubleSpinBox,QHeaderView
)
from PyQt6.QtCore import Qt, QSortFilterProxyModel
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
        self.montant=QDoubleSpinBox()
        self.montant.setMinimum(5)
        self.montant.setMaximum(1000)
        self.montant.setPrefix("$")
        self.montant.setSingleStep(5)
        self.btn_save= QPushButton("Enregistrer")
        self.btn_save.clicked.connect(self.enregistrer)
        layout_enregistrement.addRow("ID ETUDIANT",self.id_etudiant)
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
        self.champ_recherche= QLineEdit(objectName= "search")
        self.champ_recherche.setPlaceholderText("🔍 Tapez votre recherche")
        self.champ_suppression= QLineEdit()
        self.champ_suppression.setPlaceholderText("Entrez l'ID")
        self.btn_supprimer= QPushButton("Supprimer")
        self.btn_supprimer.clicked.connect(self.delete)
        self.filtrer = QComboBox()
        self.filtrer.addItems(["Filtrer...","Ancien ➡️ Récent ","Récent ➡️ Ancien "])
        self.filtrer.currentIndexChanged.connect(self.trier_table)
        menu.addWidget(self.champ_recherche, 2)
        menu.addWidget(self.champ_suppression,1)
        menu.addWidget(self.btn_supprimer,1)
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
        self.sous_onglets.setCurrentIndex(1)
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
        self.montant.setValue(0)
#-----------------------------------------------------------------------------------------------------------------------
    

    def enregistrer(self):
        id_etudiant = self.id_etudiant.text().strip()
    
        if not id_etudiant.isdigit():
            QMessageBox.warning(self, "Erreur", "⚠ L’ID doit être un nombre.")
            return
    
        if not etudiant_existe(int(id_etudiant)):
            QMessageBox.warning(self, "Erreur", "❌ Étudiant introuvable.")
            return

        montant = self.montant.value()

        message = save_paiement(
            id_etudiant=id_etudiant,
            montant=montant
            )
        QMessageBox.information(self, "Succès", message)
        self.renitialiser()
#----------------------------------------------------------------------------------------------------------------------
    def afficher(self):
        en_tete= ["ID","Nom","Promotion","ID ETUDIANT","Montant","Date Paiement"]
        requete= affichage_paiement()
        modele= QStandardItemModel(len(requete),len(en_tete))
        modele.setHorizontalHeaderLabels(en_tete)

        for row_index, ligne in enumerate(requete):
            for col_index, valeur in enumerate(ligne):
                item = QStandardItem(str(valeur).capitalize())
                modele.setItem(row_index,col_index,item)
        self.table.setModel(modele)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.setAlternatingRowColors(True)
        rechercher_proxy(self.table, self.champ_recherche,colonne=-1)


#-----------------------------------------------------------------------------------------------------------------
    def delete(self):
        id_texte= self.champ_suppression.text()
        if id_texte:
            if not id_texte.isdigit():
                QMessageBox.warning(self,"Erreur","Entrez un nombre!")
                return
            reponse= QMessageBox.question(
                self,"Suppression","Voulez-vous vraiment supprimer ce paiement?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reponse== QMessageBox.StandardButton.Yes:
                action= supprimer_paiement(id_texte)
                QMessageBox.information(self,"Succès",action)
                self.champ_suppression.clear()
            else:
                return
    def trier_table(self):
        modele= self.table.model()
        if not isinstance(modele, QSortFilterProxyModel):
            return
    

        choix= self.filtrer.currentText()

        if choix == "Ancien ➡️ Recent":
            modele.sort(5,Qt.SortOrder.AscendingOrder)
        elif choix == "Recent ➡️ Ancien":
            modele.sort(5,Qt.SortOrder.DescendingOrder)
        
    

