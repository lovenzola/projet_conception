from base_donnees.statistiques import total_paiement, total_conception, total_etudiants, total_preconception, total_reconception, paiement_complet
from PyQt6.QtWidgets import QWidget, QGroupBox,QProgressBar, QLabel, QVBoxLayout, QMainWindow, QHBoxLayout
from PyQt6.QtCore import Qt

class Onglet_fichier(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000,600)
        self.setWindowTitle("CARD GENERATOR- Statistiques")
        
        page= QWidget()
        layout= QHBoxLayout()

        menu= QWidget()
        layout_menu= QVBoxLayout()
        stats= QLabel("LES STATISTIQUES", objectName= "onglet_stats")
        stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_menu.addWidget(stats)
        menu.setLayout(layout_menu)

        page_stats= QWidget()
        layout_statistiques= QVBoxLayout()
        group_stats= QGroupBox("Statistiques", objectName= "group_principal")

        layout_stats= QVBoxLayout()

        group_etudiants= QGroupBox("Stats-Etudiants", objectName= "sous_group" )
        group_paiements= QGroupBox("Stats-Paiements", objectName= "sous_group")
        group_preconception= QGroupBox("Stats-Preconception", objectName= "sous_group")
        group_conception= QGroupBox("Stats-Conception", objectName= "sous_group")
        group_reconception= QGroupBox("Stats-Reconception", objectName= "sous_group")

        layout_etudiants= QVBoxLayout()
        total_etu= QLabel("Total étudiants enregistrés")
        self.bar_etudiant= QProgressBar()
        self.bar_etudiant.setMaximum(100)
        layout_etudiants.addWidget(total_etu)
        layout_etudiants.addWidget(self.bar_etudiant)
        group_etudiants.setLayout(layout_etudiants)

        layout_paiement= QVBoxLayout()
        total_pai= QLabel("Nombre Total de paiements")
        self.bar_paiement= QProgressBar()
        self.bar_paiement.setMaximum(100)
        pai_etudiant=  QLabel("Nombre d'Etudiants Complets")
        self.bar_etu_paye= QProgressBar()
        self.bar_etu_paye.setMaximum(100)
        layout_paiement.addWidget(total_pai)
        layout_paiement.addWidget(self.bar_paiement)
        layout_paiement.addWidget(pai_etudiant)
        layout_paiement.addWidget(self.bar_etu_paye)
        group_paiements.setLayout(layout_paiement)

        layout_precon= QVBoxLayout()
        total_precon= QLabel("Total preconceptions")
        self.bar_precon= QProgressBar()
        self.bar_precon.setMaximum(100)
        layout_precon.addWidget(total_precon)
        layout_precon.addWidget(self.bar_precon)
        group_preconception.setLayout(layout_precon)

        layout_con= QVBoxLayout()
        total_con= QLabel("Total Conception")
        self.bar_con= QProgressBar()
        self.bar_con.setMaximum(100)
        layout_con.addWidget(total_con)
        layout_con.addWidget(self.bar_con)
        group_conception.setLayout(layout_con)

        layout_recon= QVBoxLayout()
        total_recon= QLabel("Total Reconception")
        self.bar_recon= QProgressBar()
        self.bar_recon.setMaximum(100)
        layout_recon.addWidget(total_recon)
        layout_recon.addWidget(self.bar_recon)
        group_reconception.setLayout(layout_recon)
        
        layout_stats.addWidget(group_etudiants)
        layout_stats.addWidget(group_paiements)
        layout_stats.addWidget(group_preconception)
        layout_stats.addWidget(group_conception)
        layout_stats.addWidget(group_reconception)

        group_stats.setLayout(layout_stats)
        layout_statistiques.addWidget(group_stats)
        page_stats.setLayout(layout_statistiques)

        layout.addWidget(menu, 1)
        layout.addWidget(page_stats, 3)
        page.setLayout(layout)


        self.setCentralWidget(page)
        self.actualiser()

    def actualiser(self):
        total= 100
        total_etu= total_etudiants()
        total_paye= total_paiement()
        total_etu_paye= paiement_complet()
        total_precon= total_preconception()
        total_con = total_conception()
        total_recon= total_reconception()

        
        pour_etudiants= int((total_etu / total)*100) if total_etu else 0
        pour_paiement= int((total_paye / total_etu)*100) if total_paye else 0
        pour_etu_paye= int((total_etu_paye / total_etu)*100) if total_etu_paye else 0
        pour_precon= int((total_precon / total_etu)*100) if total_precon else 0
        pour_con= int((total_con / total_etu)*100) if total_con else 0
        pour_recon= int((total_recon / total_etu)*100) if total_recon else 0

        self.bar_etudiant.setValue(pour_etudiants)
        self.bar_paiement.setValue(pour_paiement)
        self.bar_etu_paye.setValue(pour_etu_paye)
        self.bar_precon.setValue(pour_precon)
        self.bar_con.setValue(pour_con)
        self.bar_recon.setValue(pour_recon)


        





