from sqlalchemy import create_engine, MetaData, Table, text, select
# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)
#------------------------------------------------------------------------------------------------------------------
# Fonction du remplissage de la table preconception avec le TRIGGER
#-----------------------------------------------------------------------------------------------------------------
def preconception ():
    try:
        script_trigger= """
        CREATE OR REPLACE FUNCTION insertion_preconception()
        RETURNS TRIGGER AS $$
        DECLARE
            total_paye NUMERIC;
            seuil_attendu NUMERIC;
            prefixe TEXT;
        BEGIN
            SELECT matricule INTO prefixe FROM etudiants WHERE id = NEW.id_etudiant;
            IF prefixe LIKE 'si%' THEN
                seuil_attendu := 970;
            ELSIF prefixe LIKE 'ae%' OR prefixe LIKE 'dr%' OR prefixe LIKE 'th%' THEN
                seuil_attendu := 915;
            ELSIF prefixe LIKE 'md%' THEN
                seuil_attendu := 965;
            END IF;
            SELECT SUM(montant)
            INTO total_paye
            FROM paiements
            WHERE id_etudiant = NEW.id_etudiant;
            IF total_paye >= seuil_attendu THEN
                IF NOT EXISTS (
                    SELECT 1 FROM preconception WHERE id_etudiant = NEW.id_etudiant
                ) THEN
                INSERT INTO preconception (id_etudiant, date_conception)
                VALUES (NEW.id_etudiant, CURRENT_DATE);
                END IF;
            END IF;
        RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trigger_verif_conception
        AFTER INSERT ON paiements
        FOR EACH ROW
        EXECUTE FUNCTION insertion_preconception();
        """
        with engine.connect() as connection:
            connection.execute(text(script_trigger))
            connection.commit()
            print("Trigger et fonction preconception executes avec succes")
    except Exception as e:
        print("Erreur survenue lors de la creation du trigger:", e)


    