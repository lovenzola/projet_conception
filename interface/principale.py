from interface.onglet_etudiant import Onglet_etudiant
from interface.onglet_paiement import Onglet_paiement
from interface.onglet_cartes import Onglet_cartes
from interface.onglet_stats import Onglet_fichier
from PyQt6.QtWidgets import QWidget,QApplication, QVBoxLayout, QTabWidget, QMainWindow, QMessageBox, QLabel, QProgressBar
from PyQt6.QtCore import Qt,QTimer
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
#---------------------------------------------------------------------------------------------------------------------
        self.deconnecter= QWidget()
        layout_deconn= QVBoxLayout()
        self.label= QLabel("Deconnexion")
        self.progressbar= QProgressBar()
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(100)
        self.progressbar.setTextVisible(False)
        self.progressbar.setValue(0)
        self.valeur=0
        self.timer= QTimer()
        self.timer.timeout.connect(self.progression)
        layout_deconn.addWidget(self.label)
        layout_deconn.addWidget(self.progressbar)
        self.deconnecter.setLayout(layout_deconn)


        self.ecran.addTab(Onglet_fichier(),"Statistiques")
        self.ecran.addTab(Onglet_etudiant(),"Etudiants")
        self.ecran.addTab(Onglet_paiement(),"Paiements")
        self.ecran.addTab(Onglet_cartes(),"Gestion Cartes")
        self.ecran.addTab(self.deconnecter,"Déconnexion")
        self.ecran.currentChanged.connect(self.deconnexion)
        self.ecran.setCurrentIndex(1)
        layout.addWidget(self.ecran)
        conteneur.setLayout(layout)
        self.setCentralWidget(conteneur)

    def deconnexion(self,index):
        nom_onglet= self.ecran.tabText(index)
        if nom_onglet == "Déconnexion":
            reponse = QMessageBox.question(
                self, "Validation", "Voulez-vous vraiment quitter l'application?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reponse == QMessageBox.StandardButton.Yes:
                self.timer.start(100)
                self.progressbar.setValue(0)
                

            else : 
                self.ecran.setCurrentIndex(1)
        
    def progression(self):
        
        if self.valeur <= 100:
            self.label.setText("Fermeture de l'application")
            self.progressbar.setValue(self.valeur)
            self.valeur += 20
        else: 
            self.timer.stop()
            self.close()
            QApplication.quit()
            



