from interface.principale import Principale
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QFormLayout, QFrame, QMainWindow, QApplication, QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt


#--------------------------------------------------------------------------------------------------------------------
class connexion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authentification")
        self.resize(800,400)
        self.setStyleSheet("font-size: 16px;font-family: sans serif;background-color: #00A1B9;color: white;")

        # DEFINITION DE L'ECRAN DE CONNEXION

        ecran_connexion= QWidget()
        layout_principal= QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)

        conteneur= QFrame()
        conteneur.setStyleSheet("""QLineEdit{background-color: #F2F7FC;color: black; border: 1px solid #0078D7 ; border-radius: 7px; margin: 8px; height: 40px;} """)
        
        formulaire= QVBoxLayout()
        self.titre= QLabel("Page connexion")
        self.titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titre.setStyleSheet("font-size: 25px; font-weight: bold; text-decoration: underline; ")
        self.nom= QLineEdit()
        self.nom.setPlaceholderText("Entrez votre nom...")
        self.code= QLineEdit()
        self.code.setPlaceholderText("Entrez le mot de passe")
        self.code.setEchoMode(QLineEdit.EchoMode.Password)
        self.bouton= QPushButton("Se connecter")
        self.bouton.clicked.connect(self.acces)
        self.bouton.setStyleSheet("font-weight:bold; height: 25px;background-color: #0078D7; color:white; border: 1px solid white; border-radius: 10px; max-width: 170px; margin-left: 100px;")
        
        formulaire.addWidget(self.titre)
        formulaire.addWidget(self.nom)
        formulaire.addWidget(self.code)
        formulaire.addWidget(self.bouton)
        
        conteneur.setLayout(formulaire)  
        conteneur.setFixedWidth(400)
        
        layout_principal.addWidget(conteneur)
        ecran_connexion.setLayout(layout_principal)
        
        self.setCentralWidget(ecran_connexion)
#-----------------------------------------------------------------------------------------------------------------
#               SIMILUTION D'UNE BASE DE DONNEES ET AUTHENTIFICATION 
#----------------------------------------------------------------------------------------------------------------
    def acces(self):

        # Dictionnaire d'informations 
        self.infos= {
            "admin1": "123456",
            "admin2" : "000000"
        }
    #------------------------------------------------------------------------------
        nom= self.nom.text()
        code= self.code.text()
        
        if nom in self.infos and self.infos[nom] == code:
            self.connecter= Principale()
            self.connecter.show()
            self.close()
        else:
            QMessageBox.warning(self, "alerte","Nom ou Mot de passe incorrect!")

        
            




