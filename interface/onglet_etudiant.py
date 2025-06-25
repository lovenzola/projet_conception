from base_donnees.historique import afficher_etudiant
from base_donnees.etudiant import save_etudiant
from PyQt6.QtWidgets import (
    QWidget, QApplication, QPushButton, QToolBox, QLabel, QVBoxLayout, QStackedWidget, QTableView, QTabWidget,
    QMainWindow, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QMessageBox,QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class Onglet_etudiant(QWidget):
    def __init__(self):
        super().__init__()
        layout_principal= QHBoxLayout(self)
#============ BARRE A GAUCHE CONTENANT LES SOUS-ONGLETS ===================================
        self.sous_onglets= QToolBox()

        sous_onglet_save= QWidget()
        sous_onglet_show= QWidget()
        self.sous_onglets.addItem(sous_onglet_save,"Enregistrer un etudiant")
        self.sous_onglets.addItem(sous_onglet_show,"Liste des etudiants")
        
#--------------------------------------------------------------------------------------------------------------------
        # LE CADRE DROIT, L'AFFICHEUR
        self.stack= QStackedWidget()
#---------------------------- PAGE ENREGISTRER ----------------------------------------------------------------------
        page_enregistrement= QWidget()
        layout_enregistrement= QFormLayout()
        self.sexe= QComboBox()
        self.sexe.addItems(["F","H"])
        self.promotion= QComboBox()
        self.promotion.addItems(["L1 LMD FASI", "L1 LMD FASE","L1 LMD DROIT","L1 LMD THEOLOGIE","G0 MEDECINE"])
        self.photo_path= QComboBox()
        self.photo_path.addItems(["C:\projet\multimedia\icone_femme_black.jpg", "C:\projet\multimedia\icone_homme_black.jpg"])
        self.date_naissance= QLineEdit()
        self.date_naissance.setPlaceholderText("YYYY-MM-DD")
        self.btn_save= QPushButton("Enregistrer")
        self.btn_save.clicked.connect(self.enregistrer)
        self.nom= QLineEdit()
        self.postnom= QLineEdit()
        self.prenom= QLineEdit()
        self.matricule= QLineEdit()
        layout_enregistrement.addRow("Nom :",self.nom)
        layout_enregistrement.addRow("Post-nom :",self.postnom)
        layout_enregistrement.addRow("Prenom :",self.prenom)
        layout_enregistrement.addRow("Matricule :",self.matricule)
        layout_enregistrement.addRow("Sexe :",self.sexe)
        layout_enregistrement.addRow("Promotion",self.promotion)
        layout_enregistrement.addRow("Date de naissance",self.date_naissance)
        layout_enregistrement.addRow("Chemin image :",self.photo_path)
        layout_enregistrement.addWidget(self.btn_save)

        page_enregistrement.setLayout(layout_enregistrement)
        
# ----------------------------------- PAGE AFFICHER --------------------------------------------------------------------
        page_afficher = QWidget()
        layout_afficher = QVBoxLayout()
        #----------------------------- DEFINITION DU MENU ------------------------------------------------------
        self.menu= QWidget()
        menu = QHBoxLayout()
        self.champ_recherche= QLineEdit()
        self.champ_recherche.setPlaceholderText("")
        self.btn_search= QPushButton("🔍 Rechercher")
        #self.btn_search.clicked.connect(self.rechercher)
        self.filtrer = QComboBox()
        self.filtrer.addItems(["Filtrer...", "Promotion","A ➡️ Z", "Z ➡️ A"])
        menu.addWidget(self.champ_recherche, 2)
        menu.addWidget(self.btn_search,2)
        menu.addWidget(self.filtrer,1)
        self.menu.setLayout(menu)

        #---------------------------- TABLEAU D'AFFICHAGE -----------------------------------------------------
        self.table= QTableView()
#-----------------------------------------------------------------------------------------------------------------------

        layout_afficher.addWidget(self.menu)
        layout_afficher.addWidget(self.table)

        page_afficher.setLayout(layout_afficher)

        self.stack.addWidget(page_enregistrement)
        self.stack.addWidget(page_afficher)
        self.sous_onglets.currentChanged.connect(self.controle_onglet)
        layout_principal.addWidget(self.sous_onglets,1)
        layout_principal.addWidget(self.stack,4)
        self.setLayout(layout_principal)

#------------------------------------------------------------------------------------------------------------------------
    def renitialiser(self):
        self.nom.clear()
        self.postnom.clear()
        self.prenom.clear()
        self.matricule.clear()
        self.sexe.setCurrentIndex(0)
        self.promotion.setCurrentIndex(0)
        self.date_naissance.clear()
        self.photo_path.clear()
#----------------------------------------------------------------------------------------------------------------------
    def enregistrer(self):
        nom= self.nom.text()
        postnom=self.postnom.text()
        prenom= self.prenom.text()
        matricule= self.matricule.text()
        sexe= self.sexe.currentText()
        promotion= self.promotion.currentText()
        date_naissance= self.date_naissance.text()
        photo_path= self.photo_path.currentText()
        message= save_etudiant(
            nom= nom.lower(),
            postnom=postnom.lower(),
            prenom=prenom.lower(),
            matricule=matricule.lower(),
            sexe=sexe.lower(),
            promotion=promotion.lower(),
            date_naissance=date_naissance.lower(),
            photo_path=photo_path
        )
        QMessageBox.information(self,"SUCCES", message)
        self.renitialiser()
#---------------------------------------------------------------------------------------------------------------------
    def afficher(self):
        en_tete= ["ID","Nom","Post-nom","Prenom","Matricule","Promotion","Sexe","Date de naissance","Photo_path"]
        requete= afficher_etudiant()
        modele= QStandardItemModel(len(requete),len(en_tete))
        modele.setHorizontalHeaderLabels(en_tete)

        for row_index, ligne in enumerate(requete):
            for col_index, valeur in enumerate(ligne):
                item = QStandardItem(str(valeur))
                modele.setItem(row_index,col_index,item)
        self.table.setModel(modele)
        self.table.resizeRowsToContents()
#--------------------------------------------------------------------------------------------------------------------
    def controle_onglet(self,index):
        self.stack.setCurrentIndex(index)
        if index == 1:
            self.afficher()            
#-----------------------------------------------------------------------------------------------------------------------