from sqlalchemy import create_engine, MetaData, Table, select, func, delete
from sqlalchemy.exc import SQLAlchemyError

# Connexion à la base de données
engine = create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection = engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)

# Tables nécessaires
preconceptions = Table('preconception', metadata, autoload_with=engine, schema='public')
conception = Table("conception", metadata, autoload_with=engine, schema="public")
etudiants = Table("etudiants", metadata, autoload_with=engine, schema="public")

# Fonctions d'importation des modèles
from modeles_carte.modeles import modele_droit, modele_fase, modele_fasi, modele_med

#----------------------------------------------------------------------------------------------------------------
#               FONCTION DE VERIFICATION SI IL Y A 10 ETUDIANTS A PAIEMENT COMPLET
#----------------------------------------------------------------------------------------------------------------
def verification_conception():
    try:
        comptage = select(func.count()).select_from(preconceptions)
        with engine.connect() as connection:
            resultat = connection.execute(comptage)
            return resultat.scalar() >= 10
    except SQLAlchemyError as e:
        print("❌ Erreur lors de la vérification :", e)
        return False

# ----------------------------------------------------------------------------------------------------------------
#                           FONCTION POUR VIDER LA TABLE PRECONCEPTION
#-----------------------------------------------------------------------------------------------------------------
def vider_preconception():
    try:
        with engine.connect() as connection:
            connection.execute(delete(preconceptions))
            connection.commit()
    except SQLAlchemyError as e:
        print("❌ Erreur lors du nettoyage de la table preconception :", e)

#---------------------------------------------------------------------------------------------------------------
#                       FONCTION POUR LANCER LA CONCEPTION
#---------------------------------------------------------------------------------------------------------------
def concevoir():
    try:
        requete = select(
            etudiants.c.matricule,
            etudiants.c.nom,
            etudiants.c.postnom,
            etudiants.c.prenom,
            etudiants.c.sexe,
            etudiants.c.promotion,
            etudiants.c.date_naissance,
            etudiants.c.photo_path,
            preconceptions.c.id_etudiant
        ).join(etudiants, etudiants.c.id == preconceptions.c.id_etudiant)

        with engine.connect() as connection:
            resultat = connection.execute(requete).fetchall()

            for row in resultat:
                prefix = row.matricule[:2].lower()
                modele = None

                # Sélection du modèle selon le préfixe
                if prefix == "si":
                    modele = "modele_fasi"
                    modele_fasi(row)
                elif prefix == "ae":
                    modele = "modele_fase"
                    modele_fase(row)
                elif prefix == "dr":
                    modele = "modele_droit"
                    modele_droit(row)
                elif prefix == "md":
                    modele = "modele_medecine"
                    modele_med(row)
                elif prefix == "th":
                    print(f"ℹ Modèle non disponible pour : {row.matricule}")
                    continue
                else:
                    print(f"⚠ Matricule invalide : {row.matricule}")
                    continue

                # Enregistrement dans la table conception
                connection.execute(
                    conception.insert().values(
                        etudiant_id=row.id_etudiant,
                        nom_modele=modele
                    )
                )
                connection.commit()

            vider_preconception()
            print("✅ Conception terminée avec succès.")

    except SQLAlchemyError as e:
        print(f"❌ Erreur lors de la conception : {e}")