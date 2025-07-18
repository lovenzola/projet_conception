from interface.connexion import connexion
from PyQt6.QtWidgets import (
    QProgressBar, QLabel, QPushButton, QVBoxLayout, QStatusBar,QWidget,QMainWindow
)
from PyQt6.QtCore import Qt, QTimer

#-------------------------------------------------------------------------------------------------------------------
#                               LE STYLE A APPLIQUER
#------------------------------------------------------------------------------------------------------------------
style= ("""
                QProgressBar{
                    margin-left: 25px;
                    border-radius: 6px;
                    background-color: #F5F5F5;
                    
                }
                QProgressBar::chunk{
                    border-radius: 5px;
                    background-color: rgba(0,120,215,0.9);
                }
                QLabel#titre{
        
                    font-size: 30px;
                    color: #FAFAFA;
                    font-weight: bold;
                    margin-left: 55px;
                }
                QPushButton{
                    background-color: rgba(0,120,215,0.7);
                    border: 2px solid white;
                    border-radius: 10px;
                    margin : 10px;
                    margin-left: 133px;
                    font-size : 20px;
                    font-weight: bold;
                    max-width: 120px;
                    height: 30px;
                    color: #FAFAFA;
               
                }
            """)
#-----------------------------------------------------------------------------------------------------------------------

class accueil(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000,600)
        self.setStyleSheet("background-color:  #00A1B9; font-family: sans serif;")

        self.accueil= QWidget()
        self.accueil.setStyleSheet(style)
        layout= QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label= QLabel("CARD GENERATOR", objectName= "titre")
        self.label.hide()

        self.progression = QProgressBar()  
        self.progression.setMinimum(0)
        self.progression.setMaximum(100)
        self.progression.setValue(0)
        self.progression.setTextVisible(False)
        self.progression.setMaximumWidth(380)
        self.progression.setFixedHeight(15)
        self.valeur= 0

        self.bouton= QPushButton("Ouvrir")
        self.bouton.clicked.connect(self.connexion)
        self.bouton.hide()

        self.message= QLabel(" \U0001F501 Chargement de l'application")
        self.message.setStyleSheet("color: #E0F7FA;font-size: 13px; padding: 10px;")
        self.setStatusBar(QStatusBar())
        self.statusBar().addWidget(self.message)
        self.statusBar().showMessage("Chargement de l'application")

        layout.addWidget(self.label)
        layout.addWidget(self.progression)
        layout.addWidget(self.bouton)
        self.accueil.setLayout(layout)
        self.timer= QTimer()
        self.timer.timeout.connect(self.affichage)

        self.setCentralWidget(self.accueil)
#----------------------------------------------------------------------------------------------------------------------
    # LANCEMENT DE LA PROGRESSION A L'OUVERTURE DE L'ECRAN 
    def showEvent(self, event):
        self.timer.start(150)
        return super().showEvent(event)
#----------------------------------------------------------------------------------------------------------------------
    # AFFICHER LES ELEMENTS DE L'ECRAN

    def affichage(self):
        if self.valeur <= 100:
            self.progression.setValue(self.valeur)
            self.valeur+= 10
        else:
            self.timer.stop()
            self.label.show()
            self.bouton.show()
            self.statusBar().setHidden(True)
#----------------------------------------------------------------------------------------------------------------------
    # CONNEXION A LA PAGE DE CONNEXION
    
    def connexion (self):
        self.connecter= connexion()
        self.connecter.show()
        self.close()



        


