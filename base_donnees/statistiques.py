from sqlalchemy import Table, MetaData, select, func, text, create_engine

engine = create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection = engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)

etudiants= Table('etudiants',metadata, autoload_with=engine, schema='public')
paiements= Table('paiements',metadata, autoload_with=engine, schema='public')
conception= Table('conception',metadata, autoload_with=engine, schema='public')
preconception= Table('preconception',metadata, autoload_with=engine, schema='public')
reconception= Table('reconception',metadata, autoload_with=engine, schema='public')

def total_etudiants():
    with engine.connect() as connection:
        resultat= connection.execute(select(func.count()).select_from(etudiants))
        return resultat.scalar()
    
def total_paiement():
    with engine.connect() as connection:
        resultat= connection.execute(select(func.count()).select_from(paiements))
        return resultat.scalar()

def paiement_complet():
    requete= """
    select count(*) from (
        select id_etudiant,
                sum(montant) as total,
                lower(replace(e.promotion,' ','')) as promo
        from paiements p
        join etudiants e on p.id_etudiant = e.id
        group by id_etudiant, promo
        having
            (lower(replace(e.promotion, ' ','')) in ('l1lmddroit','l1lmdfase','l1theologie') and sum(montant) = 915) or
            (lower(replace(e.promotion, ' ',''))  = 'l1lmdfasi' and sum(montant) = 970) or
            (lower(replace(e.promotion, ' ',''))  = 'g0medecine' and sum(montant) = 965)
        ) as paiements_complets;
    """
    with engine.connect() as connection:
        resultat= connection.execute(text(requete))
        return resultat.scalar()

def total_conception():
    with engine.connect() as connection:
        resultat= connection.execute(select(func.count()).select_from(conception))
        return resultat.scalar()

def total_preconception():
    with engine.connect() as connection:
        resultat= connection.execute(select(func.count()).select_from(preconception))
        return resultat.scalar()

def total_reconception():
    with engine.connect() as connection:
        resultat= connection.execute(select(func.count()).select_from(reconception))
        return resultat.scalar()
    


