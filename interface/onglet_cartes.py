from base_donnees.historique import afficher_conception
from base_donnees.historique import afficher_preconception
from PyQt6.QtWidgets import (
    QWidget, QApplication, QPushButton, QToolBox, QLabel, QVBoxLayout, QStackedWidget, QTableView, QTabWidget,
    QMainWindow, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QMessageBox,QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QStandardItemModel, QStandardItem
class Onglet_cartes(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(1000,600)
        self.setWindowTitle("CARD GENERATOR - Gestion des cartes")
        layout_principal= QHBoxLayout(self)
#============ BARRE A GAUCHE CONTENANT LES SOUS-ONGLETS ===================================
        self.sous_onglets= QToolBox()
        self.stack_global= QStackedWidget()
        sous_onglet_preconc= QWidget()
#--------------------------------- PAGE CONCEPTION ---------------------------------------------------
        sous_onglet_conc= QWidget()
        self.stack_cartes= QStackedWidget()
        layout_onglet_con= QVBoxLayout()
        self.btn_affichage= QPushButton("Afficher la table")
        self.btn_affichage.clicked.connect(lambda: self.affichage_pages("table"))
        self.btn_dossier= QPushButton("Dossiers Cartes")
        self.btn_dossier.clicked.connect(lambda: self.affichage_pages("dossier"))
        self.btn_concevoir= QPushButton("Espace Conception")
        layout_onglet_con.addWidget(self.btn_affichage)
        layout_onglet_con.addWidget(self.btn_dossier)
        layout_onglet_con.addWidget(self.btn_concevoir)
        sous_onglet_conc.setLayout(layout_onglet_con)
#----------------------------------------------------------------------------
        sous_onglet_recon= QWidget()

        self.sous_onglets.addItem(sous_onglet_preconc,"Table Preconception")
        self.sous_onglets.addItem(sous_onglet_conc,"Conception")
        self.sous_onglets.addItem(sous_onglet_recon,"Reconception")
        
#--------------------------------------------------------------------------------------------------------------------
        # LE CADRE DROIT, L'AFFICHEUR
        page_preconception= QWidget()
        #--------------------------------- PAGE PRECONCEPTION ---------------------------------------------------
        layout_preconception = QVBoxLayout()
        #----------------------------- DEFINITION DU MENU ------------------------------------------------------
        self.menu_precon= QWidget()
        
        #---------------------------- TABLEAU D'AFFICHAGE -----------------------------------------------------
        self.table= QTableView()
        layout_preconception.addWidget(self.menu_precon)
        layout_preconception.addWidget(self.table)
        page_preconception.setLayout(layout_preconception)
#---------------------------------------------------------------------------------------------------------
        self.page_conception= QWidget()
        self.layout_conception= QVBoxLayout()
        self.layout_conception.addWidget(self.stack_cartes)
        self.page_conception.setLayout(self.layout_conception)
#------------------------------------------------------------------------------------------------------------------
        page_reconception= QWidget()
        self.stack_global.addWidget(page_preconception)
        self.stack_global.addWidget(self.page_conception)
        self.stack_global.addWidget(page_reconception)
        
        self.sous_onglets.currentChanged.connect(self.controle_onglet)
        layout_principal.addWidget(self.sous_onglets,1)
        layout_principal.addWidget(self.stack_global,4)
        self.setLayout(layout_principal)

#------------------------------------------------------------------------------------------------------------------
    def controle_onglet(self, index):
        self.stack_global.setCurrentIndex(index)
        if index == 0:
            self.affichage_preconception()
        elif index == 1:
            self.page_conception
#------------------------------------------------------------------------------------------------------        
    def affichage_preconception(self):
        self.menu_preconcept = QHBoxLayout()
        self.champ_recherche= QLineEdit()
        self.btn_search= QPushButton("🔍 Rechercher")
        self.menu_preconcept.addWidget(self.champ_recherche, 3)
        self.menu_preconcept.addWidget(self.btn_search,1)
        self.menu_precon.setLayout(self.menu_preconcept)
        en_tete= ["ID","ID ETUDIANT","Nom","Post-nom","Statut","Date"]
        requete = afficher_preconception()

        modele= QStandardItemModel(len(requete),len(en_tete))
        modele.setHorizontalHeaderLabels(en_tete)
        modele.setHorizontalHeaderLabels(en_tete)
        for row_index, ligne in enumerate(requete):
            for col_index, valeur in enumerate(ligne):
                item= QStandardItem(str(valeur))
                modele.setItem(row_index,col_index,item)
        self.table.setModel(modele)
        self.table.resizeRowsToContents() 
#-------------------------------------------------------------------------------------------------------------------
    def affichage_conception(self):
        self.page_affichage= QWidget()
        layout_affichage= QVBoxLayout()
    #------------ DEFINITION DU MENU ------------------------------
        self.menu= QWidget()
        menu = QHBoxLayout()
        self.champ_recherche= QLineEdit()
        self.btn_search= QPushButton("🔍 Rechercher")
        menu.addWidget(self.champ_recherche, 3)
        menu.addWidget(self.btn_search,1)
        self.menu.setLayout(menu)
#---------- LA TABLE QUI AFFICHE -------------------------
        self.tableau= QTableView()

        requete = afficher_conception()
        en_tete= ["ID","ID ETUDIANT","Nom","Post-nom","Nom Modèle","Date"]
        modele= QStandardItemModel(len(requete),len(en_tete))
        modele.setHorizontalHeaderLabels(en_tete)
        for row_index, ligne in enumerate(requete):
            for col_index, valeur in enumerate(ligne):
                item= QStandardItem(str(valeur))
                modele.setItem(row_index,col_index,item)
        self.tableau.setModel(modele)
        self.tableau.resizeRowsToContents()

        layout_affichage.addWidget(self.menu)
        layout_affichage.addWidget(self.tableau)

        self.page_affichage.setLayout(layout_affichage)        

        return self.page_affichage
#----------------------------------------------------------------------------------------------------
    def affichage_pages(self,nom):
        if nom =="table":
            page= self.affichage_conception()
        elif nom == "dossier":
            page = QLabel("Voici les dossiers")
        elif nom == "carte":
            page = QLabel("Bienvenu dans l'espace connxion")
        index= self.stack_cartes.indexOf(page)
        if index == -1:
            self.stack_cartes.addWidget(page)
            self.stack_cartes.setCurrentIndex(index)

            
            
