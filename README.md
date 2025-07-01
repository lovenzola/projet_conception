#  Conception automatique des cartes d'étudiants

Ce projet est une application de bureau conçue pour automatiser l'enregistrement, la gestion et la conception de cartes d’étudiants à partir d’une base de données PostgreSQL.  
L’interface graphique est réalisée avec *PyQt6, la base de données est manipulée avec **SQLAlchemy Core, et la génération des cartes se fait en **PDF avec ReportLab*.

---

##  Fonctionnalités principales

-  Enregistrement et modification des étudiants 
-  Gestion des paiements
-  Conception automatique des cartes lorsque 10 paiements sont atteints
-  Reconception limitée à 3 fois par étudiant
-  Interface moderne
-  Écran de connexion sécurisé
-  Génération de cartes PDF avec ReportLab
-  Affichage clair et filtré des informations

---

##  Architecture du projet
projet/
│
├── base_donnees/              # Fichiers liés à la base de données et aux requêtes SQLAlchemy
│   ├── _init_.py
│   ├── conception.py
│   ├── etudiant.py
│   ├── historique.py
│   ├── paiement.py
│   ├── preconception.py
│   ├── reconception.py
│   ├── script.sql             # Script de création de la base PostgreSQL
│   └── statistique.py
│
├── cartes/                    # Dossiers de cartes générées en PDF
│   ├── carte_conception/      # Cartes créées automatiquement (1re fois)
│   └── carte_reconception/    # Cartes reconçues (modification)
│
├── interface/                 # Fichiers liés à l'interface graphique (PyQt6)
│   ├── accueil.py
│   ├── connexion.py
│   ├── fonctions_secon.py     # Fonctions secondaires (utilitaires)
│   ├── onglet_cartes.py
│   ├── onglet_etudiant.py
│   ├── onglet_paiement.py
│   ├── onglet_stats.py
│   ├── principal.py           # Fenêtre principale de l'application
│   └── themes.py              # Thème de l'application
│
├── modeles_carte/             # Modèles PDF utilisés par ReportLab
│   ├── modele_reconception.py
│   └── modeles.py
│
├── multimedia/                # Contenus visuels : logos, icônes, images
│   ├── icone_femme_black.jpg
│   ├── icone_homme_black.jpg
│   ├── logo.jpg
│   ├── logo_card_generator.jpg
│   └── logo_card_generator.ico
│
├── .gitignore                 # Fichiers/dossiers à ignorer dans Git
├── conversion_logo.py         # Script de conversion JPG → ICO
├── main.py                    # Fichier principal de lancement
├── README.md                  # Documentation du projet
└── requirements.txt           # Dépendances Python à installer

---

##  Technologies utilisées

- Python 3.13.3
- PyQt6
- PostgreSQL
- SQLAlchemy (Core)
- ReportLab
- pgAdmin
- Git

---

##  Installation et exécution

1. *Cloner le projet*
   ```bash
   git clone https://github.com/lovenzola/projet_conception.git
   cd conception-carte-etudiant

2. *Créer un environnement virtuel*
    ```bash
    python -m venv venv

3. *Activer l'environnement*

    Sous Windows : venv\Scripts\activate

4. *Installer les dépendances*
    ```bash
    pip install -r requirements.txt

5.	Configurer votre base de données PostgreSQL
	•	Nom de la base : conception_carte
	•	Utilisateur : postgres
	•	Port : 5433
	•	Mots de passe : 12345678

6. Lancer l'application
    ```bash
    python main.py

Remarques importantes
	•	La conception des cartes se déclenche automatiquement lorsque 10 étudiants sont enregistrés dans la table préconception.
	•	La reconception est limitée à 3 fois maximum par étudiant.
	•	En cas de perte de carte, les données enregistrées permettent de la régénérer facilement.

⸻

Auteur

Réalisé par NZOLA SAMBA Love
Étudiante en L1 LMD FASI, République Démocratique du Congo 
Passionnée par la conception de solutions intelligentes dans l’éducation 
