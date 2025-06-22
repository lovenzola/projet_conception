from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QFormLayout, QFrame, QMainWindow, QApplication, QVBoxLayout
)
from PyQt6.QtCore import Qt
import sys
#------------------------------------------------------------------------------------------------------------------------
style= None
#--------------------------------------------------------------------------------------------------------------------
class connexion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authentification")
        self.setMinimumSize(1000,600)
        ecran_connexion= QWidget()
        ecran_connexion.setStyleSheet("max-width: 600px; margin: 100px 100px 0 0;")
        layout_principal= QVBoxLayout()
        
        conteneur= QFrame()
        layout= QFormLayout()
        self.nom= QLineEdit()
        self.nom.setPlaceholderText("Entrez votre nom...")
        self.code= QLineEdit()
        self.code.setPlaceholderText("Entrez le mot de passe")
        self.code.setEchoMode(QLineEdit.EchoMode.Password)
        self.bouton= QPushButton("Se connecter")
        layout.addRow("NOM: ", self.nom)
        layout.addRow("MOT DE PASSE: ",self.code)
        layout.addWidget(self.bouton)
        conteneur.setLayout(layout)  
        layout_principal.addWidget(conteneur)
        ecran_connexion.setLayout(layout_principal)
        self.setCentralWidget(ecran_connexion)

app= QApplication(sys.argv)
fenetre= connexion()
fenetre.show()
sys.exit(app.exec())


