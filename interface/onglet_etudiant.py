from interface.fonctions_secon import rechercher_proxy
from base_donnees.historique import supprimer_etudiant,afficher_etudiant
from base_donnees.etudiant import save_etudiant, modifier_info
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QToolBox, QLabel, QVBoxLayout, QStackedWidget, QTableView,
    QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QMessageBox,QHeaderView
)
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem
#-----------------------------------------------------------------------------------------------------------
class Onglet_etudiant(QWidget):
    def __init__(self):
        super().__init__()
        layout_principal= QHBoxLayout(self)

    #   UNE BOITE D'ONGLETS A GAUCHE
        self.sous_onglets= QToolBox()

        sous_onglet_save= QWidget()
        sous_onglet_show= QWidget()
        sous_onglet_update= QWidget()
        self.sous_onglets.addItem(sous_onglet_save,"Enregistrer un etudiant")
        self.sous_onglets.addItem(sous_onglet_show,"Liste des etudiants")
        self.sous_onglets.addItem(sous_onglet_update, "Modifier un enregistrement")
        

    # L'EMPILATEUR DES PAGES 

        self.stack= QStackedWidget()
    #---------------------------- PAGE ENREGISTRER -----------------------------------------
        page_enregistrement= QWidget()
        layout_enregistrement= QFormLayout()
        self.sexe= QComboBox()
        self.sexe.addItems(["F","H"])

        self.promotion= QComboBox()
        self.promotion.addItems(["L1 LMD FASI", "L1 LMD FASE","L1 LMD DROIT","L1 LMD THEOLOGIE","G0 MEDECINE"])
    
        self.photo_path= QComboBox()
        self.photo_path.addItems(["C:\projet\multimedia\icone_femme_black.jpg", "C:\projet\multimedia\icone_homme_black.jpg"])
        
        self.date_naissance= QLineEdit()
        self.date_naissance.setPlaceholderText("Champ Obligatoire")

        self.btn_save= QPushButton("Enregistrer")
        self.btn_save.clicked.connect(self.enregistrer)

        self.nom= QLineEdit()
        self.nom.setPlaceholderText("Champ Obligatoire")

        self.postnom= QLineEdit()
        self.prenom= QLineEdit()

        self.matricule= QLineEdit()
        self.matricule.setPlaceholderText("Champ Obligatoire")

        layout_enregistrement.addRow("Nom :",self.nom)
        layout_enregistrement.addRow("Post-nom :",self.postnom)
        layout_enregistrement.addRow("Prenom :",self.prenom)
        layout_enregistrement.addRow("Matricule :",self.matricule)
        layout_enregistrement.addRow("Sexe :",self.sexe)
        layout_enregistrement.addRow("Promotion",self.promotion)
        layout_enregistrement.addRow("Date de naissance",self.date_naissance)
        layout_enregistrement.addRow("Chemin image :",self.photo_path)
        layout_enregistrement.addWidget(self.btn_save)

        page_enregistrement.setLayout(layout_enregistrement)
        
    # ----------------------------------- PAGE AFFICHER -----------------------------------
        page_afficher = QWidget()
        layout_afficher = QVBoxLayout()

        #----------------------------- DEFINITION DU MENU ------------------------------------------------------
        self.menu= QWidget()

        menu = QHBoxLayout()

        self.champ_recherche= QLineEdit(objectName= "search")
        self.champ_recherche.setPlaceholderText("🔍 Tapez votre recherche")

        self.champ_suppression= QLineEdit()
        self.champ_suppression.setPlaceholderText("Entrez l'ID")

        self.btn_delete=QPushButton("Supprimer")
        self.btn_delete.clicked.connect(self.delete)

        self.filtrer = QComboBox()
        self.filtrer.addItems(["Filtrer...", "A ➡️ Z", "Z ➡️ A"])
        self.filtrer.currentIndexChanged.connect(self.trier_table)

        menu.addWidget(self.champ_recherche, 2)
        menu.addWidget(self.champ_suppression,1)
        menu.addWidget(self.btn_delete,1)
        menu.addWidget(self.filtrer,1)

        self.menu.setLayout(menu)

        #---------------------------- TABLEAU D'AFFICHAGE -----------------------------------------------------
        self.table= QTableView()


        layout_afficher.addWidget(self.menu)
        layout_afficher.addWidget(self.table)

        page_afficher.setLayout(layout_afficher)
    #----------------------------------------------------------------------------------------------------------
    #                       PAGE DE MODIFICATION DES DONNEES 
    #----------------------------------------------------------------------------------------------------------
        page_modification= QWidget()
        layout_modif= QFormLayout()

        self.id_etudiant= QLineEdit()
        self.champs_autorises= QComboBox()
        self.champs_autorises.addItems(["nom","postnom","prenom","sexe","date_naissance","photo_path"])
        self.champ= QLineEdit()
        self.modification= QPushButton("Modifier")
        self.modification.clicked.connect(self.modifier_table)

        layout_modif.addRow("Entrez l'ID :",self.id_etudiant)
        layout_modif.addRow("Champ à modifier :", self.champs_autorises)
        layout_modif.addRow("Nouvelle valeur du champ :",self.champ)
        layout_modif.addWidget(self.modification)

        page_modification.setLayout(layout_modif)

        self.stack.addWidget(page_enregistrement)
        self.stack.addWidget(page_afficher)
        self.stack.addWidget(page_modification)

        self.sous_onglets.currentChanged.connect(self.controle_onglet)
        self.sous_onglets.setCurrentIndex(1)

        layout_principal.addWidget(self.sous_onglets,1)
        layout_principal.addWidget(self.stack,4)

        self.setLayout(layout_principal)

#------------------------------------------------------------------------------------------------------------------------
# FONCTION DE RENITIALISATION APRES L'ENREGISTREMENT
#-----------------------------------------------------
    def renitialiser(self):
        self.nom.clear()
        self.postnom.clear()
        self.prenom.clear()
        self.matricule.clear()
        self.sexe.setCurrentIndex(0)
        self.promotion.setCurrentIndex(0)
        self.date_naissance.clear()
        self.photo_path.clear()
#----------------------------------------------------------------------------------------------------------------------
# FONCTION D'ENREGISTREMENT
#--------------------------------------------------------
    def enregistrer(self):
        nom= self.nom.text()
        postnom=self.postnom.text()
        prenom= self.prenom.text()
        matricule= self.matricule.text()
        sexe= self.sexe.currentText()
        promotion= self.promotion.currentText()
        date_naissance= self.date_naissance.text()
        photo_path= self.photo_path.currentText()
        matricule_format= matricule.lower()
        if nom and matricule and sexe and promotion and date_naissance  and photo_path:
            if len(matricule) == 8 :
                if matricule_format[:2] in ["si","ae","dr","th","md"]:
                    message= save_etudiant(
                    nom= nom.lower(),
                    postnom=postnom.lower(),
                    prenom=prenom.lower(),
                    matricule=matricule_format,
                    sexe=sexe.lower(),
                    promotion=promotion.lower(),
                    date_naissance=date_naissance.lower(),
                    photo_path=photo_path
                    )
                    QMessageBox.information(self,"SUCCES", message)
                    self.renitialiser()
                else:
                    QMessageBox.warning(self,"Attention","Matricule invalide!")
                    return
            else:
                QMessageBox.warning(self,"Attention","Votre matricule doit comporter 8 caractères!")
                return
        else:
            QMessageBox.warning(self,"Attention","Veuillez remplir les champs obligatoires!!")
            return
#---------------------------------------------------------------------------------------------------------------------
# FONCTION D'AFFICHAGE DES ETUDIANTS DANS LA TABLE 
#------------------------------------------------------------------
    def afficher(self):
        en_tete= ["ID","Nom","Post-nom","Prenom","Matricule","Promotion","Sexe","Date de naissance","Date Enregistrement","Photo_path"]
        requete= afficher_etudiant()
        modele= QStandardItemModel(len(requete),len(en_tete))
        modele.setHorizontalHeaderLabels(en_tete)

        for row_index, ligne in enumerate(requete):
            for col_index, valeur in enumerate(ligne):
                item = QStandardItem(str(valeur).capitalize())
                modele.setItem(row_index,col_index,item)
        self.table.setModel(modele)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.setAlternatingRowColors(True)
        

        rechercher_proxy(self.table, self.champ_recherche, colonne=-1)
#--------------------------------------------------------------------------------------------------------------------
# FONCTION POUR PASSER D'UNE PAGE A L'AUTRE
#------------------------------------------------------------------------------
    def controle_onglet(self,index):
        self.stack.setCurrentIndex(index)
        if index == 1:
            self.afficher()            
#-----------------------------------------------------------------------------------------------------------------------
# FONCTION POUR SUPPRIMER 
#-----------------------------------------------------
    def delete(self):
        id_texte= self.champ_suppression.text()
        if id_texte:
            if not id_texte.isdigit():
                QMessageBox.warning(self,"Erreur","Entrez un nombre!")
                return
            reponse= QMessageBox.question(
                self,"Suppression","Voulez-vous vraiment supprimer ce paiement?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reponse== QMessageBox.StandardButton.Yes:
                action= supprimer_etudiant(id_texte)
                QMessageBox.information(self,"Succès",action)
                self.champ_suppression.clear()
            else:
                return

#-----------------------------------------------------------------------------------------------
#   FONCTION TRIER LA TABLE
#------------------------------------------------------------------------------------------------
    def trier_table(self):
        modele= self.table.model()
        if not isinstance(modele, QSortFilterProxyModel):
            return

        choix= self.filtrer.currentText()

        if choix == "A ➡️ Z":
            modele.sort(1,Qt.SortOrder.AscendingOrder)
        elif choix == "Z ➡️ A":
            modele.sort(1,Qt.SortOrder.DescendingOrder)
#-----------------------------------------------------------------------------------------------------------
#                        FONCTION POUR MODIFIER LA TABLE
#-----------------------------------------------------------------------------------------------------------
    def modifier_table(self):
        id_etudiant= self.id_etudiant.text()
        champ= self.champs_autorises.currentText().strip().lower()
        valeur= self.champ.text().strip().lower()

        if id_etudiant and champ and valeur:
            if not id_etudiant.isdigit():
                QMessageBox.warning(self,"Attention", "⛔ Entrez un nombre!")
                return
            else:
                action= modifier_info(id_etudiant, champ, valeur)
                QMessageBox.information(self,"Succès",action)
                self.champs_autorises.currentIndex()
                self.id_etudiant.clear()
                self.champ.clear()
        else:
            QMessageBox.warning(self,"Attention","⛔ Veuillez remplir les champs!")
            return
        

