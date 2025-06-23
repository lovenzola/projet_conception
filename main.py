from PyQt6.QtWidgets import QApplication
from interface.accueil import accueil
import sys
application= QApplication(sys.argv)
fenetre= accueil()
fenetre.show()
if __name__== "__main__":
    sys.exit(application.exec())
