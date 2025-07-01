from interface.onglet_etudiant import Onglet_etudiant
from interface.onglet_paiement import Onglet_paiement
from interface.onglet_cartes import Onglet_cartes
from interface.onglet_stats import Onglet_fichier
from interface.themes import THEME
from PyQt6.QtWidgets import QWidget,QLabel,QApplication, QVBoxLayout, QTabWidget, QMainWindow, QMessageBox

#                       PAGE QUI CONTIENT TOUS LES AUTRES ONGLETS
#----------------------------------------------------------------------------------------------------------
class Principale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000,600)
        self.setWindowTitle("CARD GENERATOR")
        self.setStyleSheet(THEME)
        conteneur= QWidget()
        layout= QVBoxLayout()
        self.ecran= QTabWidget()
        
        # DEFINITION DE L'ONGLET DECONNNEXION
        #------------------------------------
        self.deconnexion= QWidget()
        self.layout_deconnexion= QVBoxLayout()
        self.layout_deconnexion.addWidget(QLabel("Deconnexion"))

        # AJOUT DES ONGLETS DANS LE TABWIDGET
        #------------------------------------

        self.ecran.addTab(Onglet_fichier(),"Statistiques")
        self.ecran.addTab(Onglet_etudiant(),"Etudiants")
        self.ecran.addTab(Onglet_paiement(),"Paiements")
        self.ecran.addTab(Onglet_cartes(),"Gestion Cartes")
        self.ecran.addTab(self.deconnexion,"Deconnexion")
        self.ecran.currentChanged.connect(self.controle_onglet)
        self.ecran.setCurrentIndex(1)

        
        layout.addWidget(self.ecran)
        layout.addStretch()
        conteneur.setLayout(layout)
        self.setCentralWidget(conteneur)
#------------------------------------------------------------------------------------------------------------
    def controle_onglet(self,index):
        if index==4:
            self.deconnecter()

#---------------------------------------------------------------------------------------------------------------
#                                 FONCTION POUR DECONNEXION
#---------------------------------------------------------------------------------------------------------------
    def deconnecter(self):
        reponse = QMessageBox.question(
            self,"Deconnexion","Voulez-vous vraiment quitter l'application?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reponse == QMessageBox.StandardButton.Yes:
            self.close()
            QApplication.quit()
        else:
            self.ecran.setCurrentIndex(1)



        
    