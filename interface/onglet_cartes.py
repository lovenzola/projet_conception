from base_donnees.reconception import reconcevoir
from base_donnees.reconception import verification_reconception
from base_donnees.conception import verification_conception
from base_donnees.conception import concevoir
from base_donnees.historique import afficher_conception, afficher_preconception, afficher_reconception
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QToolBox, QVBoxLayout, QStackedWidget, QTableView,
    QHBoxLayout, QLineEdit, QMessageBox, QFormLayout
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
class Onglet_cartes(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1000, 600)
        self.setWindowTitle("CARD GENERATOR - Gestion des cartes")

        layout_principal = QHBoxLayout(self)

        # ========== TOOLBOX GAUCHE ============
        self.sous_onglets = QToolBox()
        bouton_preconception = QWidget()
        bouton_conception = QWidget()
        bouton_reconception = QWidget()
        self.sous_onglets.addItem(bouton_preconception, "Préconception")
        self.sous_onglets.addItem(bouton_conception, "Conception")
        self.sous_onglets.addItem(bouton_reconception, "Reconception")

        # ========== STACK GLOBAL ============
        self.stack_global = QStackedWidget()

        # ---------- PAGE PRECONCEPTION ----------
        self.page_preconception = QWidget()
        layout_precon = QVBoxLayout()
        self.menu_precon = QWidget()
        menu_layout = QHBoxLayout()
        self.champ_recherche = QLineEdit()
        self.btn_search = QPushButton("🔍 Rechercher")
        menu_layout.addWidget(self.champ_recherche, 3)
        menu_layout.addWidget(self.btn_search, 1)
        self.menu_precon.setLayout(menu_layout)
        self.table = QTableView()
        layout_precon.addWidget(self.menu_precon)
        layout_precon.addWidget(self.table)
        self.page_preconception.setLayout(layout_precon)

        # ---------- PAGE CONCEPTION AVEC STACK_CARTES ----------
        self.page_conception = QWidget()
        layout_conception = QVBoxLayout()
        
        boutons = QHBoxLayout()
        btn_table = QPushButton("Afficher la table")
        btn_dossier = QPushButton("Dossier Cartes")
        btn_concevoir = QPushButton("Espace Conception")
        boutons.addWidget(btn_table)
        boutons.addWidget(btn_dossier)
        boutons.addWidget(btn_concevoir)

        self.stack_cartes = QStackedWidget()
        self.page_vide = QWidget()
        layout= QVBoxLayout()
        btn_lancer_conception= QPushButton("🌟 Lancer la conception")
        btn_lancer_conception.clicked.connect(self.page_conception_carte)
        layout.addWidget(btn_lancer_conception)
        self.page_vide.setLayout(layout)
        self.stack_cartes.addWidget(self.page_affichage_cartes())
        self.stack_cartes.addWidget(self.page_dossier())
        self.stack_cartes.addWidget(self.page_vide) # Une page vide tant que le bouton n'est pas cliqué

        btn_table.clicked.connect(lambda: self.stack_cartes.setCurrentIndex(0))
        btn_dossier.clicked.connect(lambda: self.stack_cartes.setCurrentIndex(1))
        btn_concevoir.clicked.connect(lambda: self.stack_cartes.setCurrentIndex(2))

        layout_conception.addLayout(boutons)
        layout_conception.addWidget(self.stack_cartes)
        self.page_conception.setLayout(layout_conception)

        # ---------- PAGE RECONCEPTION ----------
        self.page_reconception = QWidget()
        layout_reconc = QVBoxLayout()

        boutons_reconception = QHBoxLayout()
        btn_table_reconception= QPushButton("Afficher la table")
        btn_espace_reconception= QPushButton("Espace Reconception")

        boutons_reconception.addWidget(btn_table_reconception)
        boutons_reconception.addWidget(btn_espace_reconception)
        self.page_reconception.setLayout(layout_reconc)

        self.stack_reconception= QStackedWidget()
        self.stack_reconception.addWidget(self.page_reconception_carte())
        self.stack_reconception.addWidget(self.test_reconception())
        
        btn_table_reconception.clicked.connect(lambda: self.stack_reconception.setCurrentIndex(0))
        btn_espace_reconception.clicked.connect(lambda: self.stack_reconception.setCurrentIndex(1))
        
        layout_reconc.addLayout(boutons_reconception)
        layout_reconc.addWidget(self.stack_reconception)
        self.page_reconception.setLayout(layout_reconc)

        # ========== AJOUT AU STACK GLOBAL ============
        self.stack_global.addWidget(self.page_preconception)
        self.stack_global.addWidget(self.page_conception)
        self.stack_global.addWidget(self.page_reconception)

        layout_principal.addWidget(self.sous_onglets, 1)
        layout_principal.addWidget(self.stack_global, 4)
        self.setLayout(layout_principal)

        self.sous_onglets.currentChanged.connect(self.controle_onglet)

    def controle_onglet(self, index):
        self.stack_global.setCurrentIndex(index)
        if index == 0:
            self.affichage_preconception()

    def affichage_preconception(self):
        entetes = ["ID","Nom", "Post-nom", "ID ETUDIANT", "Statut", "Date"]
        requete = afficher_preconception()
        modele = QStandardItemModel(len(requete), len(entetes))
        modele.setHorizontalHeaderLabels(entetes)
        for row, ligne in enumerate(requete):
            for col, val in enumerate(ligne):
                modele.setItem(row, col, QStandardItem(str(val)))
        self.table.setModel(modele)
        self.table.resizeColumnsToContents()

    def page_affichage_cartes(self):
        page = QWidget()
        layout = QVBoxLayout()
        table = QTableView()

        entetes = ["ID","ID ETUDIANT", "Nom", "Post-nom","Nom Modèle", "Date"]
        requete = afficher_conception()
        modele = QStandardItemModel(len(requete), len(entetes))
        modele.setHorizontalHeaderLabels(entetes)
        for row, ligne in enumerate(requete):
            for col, val in enumerate(ligne):
                modele.setItem(row, col, QStandardItem(str(val)))
        table.setModel(modele)
        table.resizeColumnsToContents()

        layout.addWidget(table)
        page.setLayout(layout)
        return page

    def page_dossier(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("📂 Ouvrir le dossier"))
        page.setLayout(layout)
        return page

    def page_conception_carte(self):
        page = QWidget()
        layout = QVBoxLayout()
        if verification_conception():
            message= QMessageBox.question(
                self, "Lancement de la conception...",
                "10 étudiants prêts. Voulez-vous générer les cartes ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if message ==QMessageBox.StandardButton.Yes:
                concevoir()
                QMessageBox.information(self,"Succès","Cartes conçues avec succès ✅")
            else:
                QMessageBox.information(self,"Annuler","⛔ La conception a été annulée")
        else:
            QMessageBox.warning(self, "Erreur", "❌ Nombre d'étdiants pas encore atteint!")
        page.setLayout(layout)
        return page

    def page_reconception_carte(self):
        page = QWidget()
        layout = QVBoxLayout()
        table = QTableView()

        entetes = ["ID","ID ETUDIANT", "Nom", "Post-nom","Nom Modèle", "Date"]
        requete = afficher_reconception()
        modele = QStandardItemModel(len(requete), len(entetes))
        modele.setHorizontalHeaderLabels(entetes)
        for row, ligne in enumerate(requete):
            for col, val in enumerate(ligne):
                modele.setItem(row, col, QStandardItem(str(val)))
        table.setModel(modele)
        table.resizeColumnsToContents()

        layout.addWidget(table)
        page.setLayout(layout)
        return page
    
    def test_reconception(self):
        page= QWidget()
        layout= QFormLayout()
        self.id_etudiant= QLineEdit()
        bouton_reconcevoir= QPushButton("Reconception")
        bouton_reconcevoir.clicked.connect(self.lancer_reconception)
        layout.addRow("ID ETUDIANT :", self.id_etudiant)
        layout.addWidget(bouton_reconcevoir)
        page.setLayout(layout)
        return page
    def lancer_reconception(self):
        etudiant_id = self.id_etudiant.text()
        verification= verification_reconception(etudiant_id)
        if verification:
            reponse= QMessageBox.question(self, "Validité","Eligible à la reconception. Voulez-vous reconcevoir ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reponse == QMessageBox.StandardButton.Yes:
                reconcevoir()
                QMessageBox.information(self,"Succès","Reconception réussie! ✅")
                
            else:
                QMessageBox.information(self,"Annulation","Reconception annulée ⛔ ")
        else:
            QMessageBox.warning(self,"Erreur","❌  Limite atteinte! Pas eligible")
        
            
            
            


