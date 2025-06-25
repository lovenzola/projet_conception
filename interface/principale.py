from interface.onglet_etudiant import Onglet_etudiant
from interface.onglet_paiement import Onglet_paiement
from interface.onglet_cartes import Onglet_cartes
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QMainWindow
class Principale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000,600)
        self.setWindowTitle("CARD GENERATOR")
        conteneur= QWidget()
        layout= QVBoxLayout()
        self.ecran= QTabWidget()
        self.setStyleSheet(
            """
                font-size: 14px;
                background-color: #FAFAFA;
            """
        )
#----------------------------------------------------------------------------------------------------------------------
        # Definition des onglets
#---------------------------------------------------------------------------------------------------------------------
        self.onglet_fichier= QWidget()
#-----------------------------------------------------------------------------------------------------------------------
        #self.onglet_etudiant= QWidget()
#----------------------------------------------------------------------------------------------------------------------        
        #self.onglet_paiement= QWidget()
#----------------------------------------------------------------------------------------------------------------------
        #self.onglet_cartes= QWidget()
#----------------------------------------------------------------------------------------------------------------------
        self.onglet_param= QWidget()
#---------------------------------------------------------------------------------------------------------------------
        self.ecran.addTab(self.onglet_fichier,"Fichier")
        self.ecran.addTab(Onglet_etudiant(),"Etudiants")
        self.ecran.addTab(Onglet_paiement(),"Paiements")
        self.ecran.addTab(Onglet_cartes(),"Gestion Cartes")
        self.ecran.addTab(self.onglet_param,"Paramètres")
        self.ecran.setCurrentIndex(1)
        layout.addWidget(self.ecran)
        conteneur.setLayout(layout)
        self.setCentralWidget(conteneur)


