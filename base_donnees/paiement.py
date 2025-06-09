from sqlalchemy import create_engine, MetaData, Table, bindparam, insert
# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)
# Accès à la table paiements
paiements= Table('paiements', metadata, autoload_with=engine, schema='public')
#--------------------------------------------------------------------------------------------------------------------
# Fonction enregistrement des paiements
#-------------------------------------------------------------------------------------------------------------------
def enregistrer_paiement(id_etudiant, montant):
    try:
        insertion= paiements.insert().values(
           id_etudiant= bindparam('id_etudiant'),
           montant= bindparam('montant'),
        )
        data= {
            "id_etudiant": id_etudiant,
            "montant": montant,
        }

        with engine.connect() as connection:
            connection.execute(insertion, data)
            connection.commit()
            print("Paiement enregistré avec succes!")
        
    except Exception as e :
        print("Erreur lors de l'enregistrement: ",e)
#------------------------------------------------------------------------------------------------------------------------
#Fonction pour lister tous les paiements faits 
#------------------------------------------------------------------------------------------------------------------------
from sqlalchemy import select, join
from base_donnees.etudiant import etudiants
def affichage_paiement():
    try:
        liste_total= select(
            paiements.c.id,
            etudiants.c.nom,
            etudiants.c.matricule,
            paiements.c.id_etudiant,
            paiements.c.montant,
            paiements.c.date_paiement
        ).join(
            etudiants, paiements.c.id_etudiant == etudiants.c.id).order_by(paiements.c.date_paiement)

        with engine.connect() as connection:
            resultat= connection.execute(liste_total)
            return resultat.fetchall()
    except Exception as e :
        print("Erreur lors de l'affichage: ", e)
#-------------------------------------------------------------------------------------------------------------------------
# Fonction pour lister le total par etudiant
#-------------------------------------------------------------------------------------------------------------------------
from sqlalchemy import select, func
def total_par_etudiant():
    try:
        total= (
            select(
                paiements.c.id_etudiant,
                etudiants.c.nom,
                etudiants.c.postnom,
                etudiants.c.prenom,
                func.sum(paiements.c.montant).label("total_paye")
            )
            .join(etudiants, paiements.c.id_etudiant == etudiants.c.id)
            .group_by(paiements.c.id_etudiant,etudiants.c.nom,etudiants.c.postnom,etudiants.c.prenom)
            .order_by(paiements.c.id_etudiant))
        
        with engine.connect() as connection:
            resultat= connection.execute(total)
            return resultat.fetchall()
    except Exception as e:
        print("Erreur survenue lors de l'affcihae:",e)

