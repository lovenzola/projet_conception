import os
import subprocess
import platform
from interface.fonctions_secon import rechercher_proxy
from base_donnees.reconception import reconcevoir
from base_donnees.reconception import verifier_tentative
from base_donnees.reconception import verification_reconception
from base_donnees.conception import verification_conception
from base_donnees.conception import concevoir
from base_donnees.historique import afficher_conception, afficher_preconception, afficher_reconception
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QToolBox, QVBoxLayout, QStackedWidget, QTableView,QHeaderView,
    QHBoxLayout, QLineEdit, QMessageBox, QFormLayout
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
class Onglet_cartes(QWidget):
    def __init__(self):
        super().__init__(),
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
        self.page_preconception= QWidget()
        layout_precon= QVBoxLayout()
        self.menu_precon = QWidget()
        menu_layout = QHBoxLayout()
        self.champ_recherche = QLineEdit(objectName= "search")
        self.champ_recherche.setPlaceholderText("🔍 Tapez votre recherche")
        menu_layout.addWidget(self.champ_recherche)
        self.menu_precon.setLayout(menu_layout)

        self.table_preconception= QTableView()

        layout_precon.addWidget(self.menu_precon)
        layout_precon.addWidget(self.table_preconception)
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
        btn_table_dossier= QPushButton("Dossier Cartes")
        btn_espace_reconception= QPushButton("Espace Reconception")

        boutons_reconception.addWidget(btn_table_reconception)
        boutons_reconception.addWidget(btn_table_dossier)
        boutons_reconception.addWidget(btn_espace_reconception)
        self.page_reconception.setLayout(layout_reconc)

        self.stack_reconception= QStackedWidget()
        self.stack_reconception.addWidget(self.page_reconception_carte())
        self.stack_reconception.addWidget(self.page_dossier_reconception())
        self.stack_reconception.addWidget(self.test_reconception())
        
        btn_table_reconception.clicked.connect(lambda: self.stack_reconception.setCurrentIndex(0))
        btn_table_dossier.clicked.connect(lambda: self.stack_reconception.setCurrentIndex(1))
        btn_espace_reconception.clicked.connect(lambda: self.stack_reconception.setCurrentIndex(2))
        
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
        self.sous_onglets.setCurrentIndex(1)
      
        liste_boutons= [btn_table, btn_dossier, btn_concevoir, btn_table_reconception, btn_table_dossier, btn_espace_reconception]
        for bouton in liste_boutons:
            bouton.setCheckable(True)
            bouton.setAutoExclusive(True)
#----------------------------------------------------------------------------------------------------------------
    def controle_onglet(self, index):
        self.stack_global.setCurrentIndex(index)
        if index == 0:
            self.affichage_preconception()
        elif index == 1:
            self.stack_cartes.removeWidget(self.stack_cartes.widget(0))
            self.stack_cartes.insertWidget(0, self.page_affichage_cartes())
            self.stack_cartes.setCurrentIndex(0)

        elif index == 2:
            self.stack_reconception.removeWidget(self.stack_reconception.widget(0))
            self.stack_reconception.insertWidget(0, self.page_reconception_carte())
            self.stack_reconception.setCurrentIndex(0)
#-------------------------------------------------------------------------------------------------------------
#                           AFFICHAGE TABLE PRECONCEPTION
#--------------------------------------------------------------------------------------------------------------
    def affichage_preconception(self):
        entetes = ["ID","Nom", "Post-nom", "ID ETUDIANT", "Statut", "Date"]
        requete = afficher_preconception()
        modele = QStandardItemModel(len(requete), len(entetes))
        modele.setHorizontalHeaderLabels(entetes)
        for row, ligne in enumerate(requete):
            for col, val in enumerate(ligne):
                modele.setItem(row, col, QStandardItem(str(val).capitalize()))
        self.table_preconception.setModel(modele)
        self.table_preconception.resizeColumnsToContents()

        rechercher_proxy(self.table_preconception,self.champ_recherche, colonne=-1)

#-------------------------------------------------------------------------------------------------------------
#                           AFFICHAGE CONCEPTION
#-------------------------------------------------------------------------------------------------------------
#      1. Table conception                                            
#----------------------------------------------------------------------
    def page_affichage_cartes(self):
        page = QWidget()
        layout = QVBoxLayout()
        menu= QWidget()
        menu_con = QHBoxLayout()
        self.searcher = QLineEdit(objectName= "search")
        self.searcher.setPlaceholderText("🔍 Tapez votre recherche")
        menu_con.addWidget(self.searcher)

        menu.setLayout(menu_con)
        self.table = QTableView()
        layout.addWidget(menu)
        page.setLayout(layout)
        table = QTableView()

        entetes = ["ID","ID ETUDIANT", "Nom", "Post-nom","Nom Modèle", "Date"]
        requete = afficher_conception()
        modele = QStandardItemModel(len(requete), len(entetes))
        modele.setHorizontalHeaderLabels(entetes)
        for row, ligne in enumerate(requete):
            for col, val in enumerate(ligne):
                modele.setItem(row, col, QStandardItem(str(val).capitalize()))
        table.setModel(modele)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        table.setAlternatingRowColors(True)
        rechercher_proxy(table,self.searcher, colonne=-1)
        layout.addWidget(menu)
        layout.addWidget(table)
        page.setLayout(layout)
        return page

#   2. Dossier des cartes conçues
#----------------------------------------------------------------------------------------------------------
    def page_dossier(self):
        page = QWidget()
        layout = QVBoxLayout()
        ouvrir_dossier= QPushButton("📂 Ouvrir le dossier")
        ouvrir_dossier.clicked.connect(lambda: self.afficher_dossier("C:\projet\cartes\carte_conception"))
        layout.addWidget(ouvrir_dossier)
        page.setLayout(layout)
        return page

#   3. FONCTION POUR LANCER LA CONCEPTION
#--------------------------------------------------------------------------------------------------------
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
                self.stack_cartes.removeWidget(self.stack_cartes.widget(0))
                self.stack_cartes.insertWidget(0,self.page_affichage_cartes())
                self.stack_cartes.setCurrentIndex(0)
            else:
                QMessageBox.information(self,"Annuler","⛔ La conception a été annulée")
        else:
            QMessageBox.warning(self, "Erreur", "❌ Nombre d'étudiants pas encore atteint!")
        page.setLayout(layout)
        return page
#-----------------------------------------------------------------------------------------------------------
#                                   TABLE RECONCEPTION
#-----------------------------------------------------------------------------------------------------------
#   1. Affichage de la table
#-----------------------------------------------------------------------------------------------------------
    def page_reconception_carte(self):
        page = QWidget()
        layout = QVBoxLayout()
        menu= QWidget()
        menu_recon = QHBoxLayout()
        self.recherche = QLineEdit(objectName= "search")
        self.recherche .setPlaceholderText("🔍 Tapez votre recherche")
        menu_recon.addWidget(self.recherche )
       

        menu.setLayout(menu_recon)
        self.table = QTableView()
        layout.addWidget(menu)
        page.setLayout(layout)
    
        table = QTableView()

        entetes = ["ID","ID ETUDIANT", "Nom", "Post-nom","Tentative", "Date"]
        requete = afficher_reconception()
        modele = QStandardItemModel(len(requete), len(entetes))
        modele.setHorizontalHeaderLabels(entetes)
        for row, ligne in enumerate(requete):
            for col, val in enumerate(ligne):
                modele.setItem(row, col, QStandardItem(str(val).capitalize()))
        table.setModel(modele)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        table.setAlternatingRowColors(True)
        rechercher_proxy(table, self.recherche , colonne=-1)
        layout.addWidget(menu)
        layout.addWidget(table)
        page.setLayout(layout)
        return page

#   2. FONCTION POUR TESTER L'ELIGIBILITE A LA RECONCEPTION
#-----------------------------------------------------------------------------------------------------------
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

#   3. FONCTION POUR LANCEMENT DE LA RECONCEPTION
#-----------------------------------------------------------------------------------------------------------
    def lancer_reconception(self):
        id_texte = self.id_etudiant.text().strip()
        if not id_texte:
            QMessageBox.warning(self,"Erreur","Erreur veillez entrer un ID" )
            return
        if not id_texte.isdigit():
            QMessageBox.critical(self,"Erreur","Vous devez entrer un nombre entier")
        try:
            etudiant_id= int(id_texte)
            if verification_reconception(etudiant_id):
                reponse =QMessageBox.question(self,"Validité","Etudiant éligible! Voulez-vous reconcevoir ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
                )
                if reponse == QMessageBox.StandardButton.Yes:
                    tentative= verifier_tentative(etudiant_id)
                    reconcevoir(etudiant_id)
                    QMessageBox.information(self,"Succès",f"Carte n°{tentative} conçue avec succès!")
                    self.stack_reconception.removeWidget(self.stack_reconception.widget(0))
                    self.stack_reconception.insertWidget(0,self.page_reconception_carte())
                    self.stack_reconception.setCurrentIndex(0)
                    self.id_etudiant.clear()
                else:
                    QMessageBox.information(self,"Annulation","Reconception annulée!")
                    self.id_etudiant.clear()
            else:
                QMessageBox.warning(self,"Echec","Etudiant non trouvé ou limite atteinte!")
                
        except ValueError:
            QMessageBox.critical(self,"Erreur","Vous devez entrer un nombre!")
        
        except Exception as e:
            QMessageBox.critical(self,"Erreur inattendue", f"Erreur survenue :\n{e}")   

#       4. FONCTION POUR ACCEDER AU DOSSIER DE CARTES RECCONCUES
#-----------------------------------------------------------------------------------------------------------
    def page_dossier_reconception(self):
        page= QWidget()
        layout= QVBoxLayout()
        ouvrir_dossier= QPushButton("📂 Ouvrir Dossier") 
        ouvrir_dossier.clicked.connect(lambda: self.afficher_dossier("C:\projet\cartes\carte_reconception"))
        layout.addWidget(ouvrir_dossier)
        page.setLayout(layout)
        return page

#-----------------------------------------------------------------------------------------------------------
#                   FONCTION POUR OUVRIR LES DOSSIERS
#-----------------------------------------------------------------------------------------------------------
    def afficher_dossier(self,path):
        if not os.path.exists(path):
            QMessageBox.warning(self, "Erreur", "❌ Le dossier n'existe pas encore")
            return
        if platform.system() == "Windows":
            os.startfile(os.path.abspath(path))
        elif platform.system() == "Darwin":
            subprocess.Popen(["open",path])
        else:
            subprocess.Popen(["xdg-open",path])
        
    
