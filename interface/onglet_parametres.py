from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt6.QtCore import pyqtSignal

class Onglet_parametres(QWidget):
    
    quitter= pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.deconnexion= QPushButton("Déconnexion")
        self.deconnexion.clicked.connect(self.deconnecter)

        self.setLayout(layout)
    
    def deconnecter(self):
        reponse = QMessageBox.question(
            self,"Deconnexion","Voulez-vous vraiment quitter l'application?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reponse == QMessageBox.StandardButton.Yes:
            self.quitter.emit()
