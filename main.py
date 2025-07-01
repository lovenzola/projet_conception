from PyQt6.QtWidgets import QApplication
from interface.accueil import accueil
import sys

if __name__== "__main__":
    application= QApplication(sys.argv)
    fenetre= accueil()
    fenetre.show()
    sys.exit(application.exec())
