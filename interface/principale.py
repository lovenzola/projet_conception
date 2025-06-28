from interface.onglet_etudiant import Onglet_etudiant
from interface.onglet_paiement import Onglet_paiement
from interface.onglet_cartes import Onglet_cartes
from interface.onglet_stats import Onglet_fichier
from interface.onglet_parametres import Onglet_parametres
from interface.themes import THEME
from PyQt6.QtWidgets import QWidget,QApplication, QVBoxLayout, QTabWidget, QMainWindow, QMessageBox, QLabel, QProgressBar
from PyQt6.QtCore import Qt,QTimer
class Principale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000,600)
        self.setWindowTitle("CARD GENERATOR")
        self.setStyleSheet(THEME)
        conteneur= QWidget()
        layout= QVBoxLayout()
        self.ecran= QTabWidget()
        
#---------------------------------------------------------------------------------------------------------------------
    

        self.ecran.addTab(Onglet_fichier(),"Statistiques")
        self.ecran.addTab(Onglet_etudiant(),"Etudiants")
        self.ecran.addTab(Onglet_paiement(),"Paiements")
        self.ecran.addTab(Onglet_cartes(),"Gestion Cartes")
        
        self.onglet_params= Onglet_parametres()
        self.onglet_params.quitter.connect(self.quitter_app)
        self.ecran.addTab(self.onglet_params,"Paramètres")
        self.ecran.setCurrentIndex(1)
        layout.addWidget(self.ecran)
        conteneur.setLayout(layout)
        self.setCentralWidget(conteneur)
    
    def quitter_app(self):
        self.close()
        QApplication.quit()
    