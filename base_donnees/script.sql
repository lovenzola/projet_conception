/* Creation des tables */
/* TABLE ETUDIANTS*/
create table if not exists etudiants (
id serial primary key,
nom varchar(50) not null,
postnom varchar(50),
prenom varchar(50),
matricule varchar(8) unique not null,
promotion varchar(20)
)

/* TABLE PAIEMENTS*/
create table if not exists paiements(
id serial primary key,
id_etudiant int not null references etudiants(id) on delete cascade,
montant numeric(10,2) not null,
date_paiement date default current_date
)

/* MODELES CARTES */
create table if not exists modeles_cartes(
id serial primary key,
nom_modele varchar(20) not null,
chemin_modele text not null,
actif boolean default false,
date_creation timestamp default current_timestamp
)

/* TABLE CONCEPTION */
create table if not exists conception(
id serial primary key,
etudiant_id integer not null references etudiants(id) on delete cascade,
date_conception timestamp default current_timestamp,
modele_id integer references modeles_cartes(id),
chemin_carte text
)

/* TABLE RECONCEPTION*/
create table if not exists reconception(
id serial primary key,
etudiant_id integer not null references etudiants(id) on delete cascade,
date_reconception timestamp default current_timestamp
)

/* Insertion des données dans la table etudiants*/
select * from etudiants 

insert into etudiants (nom,postnom,prenom,matricule,promotion)
values('nzola','samba','love','si013724','l1 lmd fasi'),
('delohim','sulemani','eclat-gabriella','si089234','l1 lmd fasi'),
('teto','filoreto','christian','si756122','l1 lmd fasi'),
('mbuyu','ilunga','franck','si431290','l1 lmd fasi'),
('nguimbi','lolo','divine','si561908','l1 lmd fasi'),
('madidi','imunga','toussaint','si756041','l1 lmd fasi'),
('kalala','odia','princesse','si879525','l1 lmd fasi'),
('musadi','kadima','theodora','si091234','l1 lmd fasi'),
('longo','longo','ainsi','si103002','l1 lmd fasi'),
('kipaka',null,'michel','si750192','l1 lmd fasi')
/* J'ai dû vider mes tables pour ajouter des colonnes à la table etudiants*/
truncate table etudiants, paiements, conception, reconception restart identity cascade 
/* Ajout des deux colonnes */
alter table etudiants
add column sexe char(1),
add column date_naissance date ;
/* Reinsertion */
select *from etudiants
insert into etudiants (nom,postnom,prenom,matricule,promotion, sexe, date_naissance)
values('nzola','samba','love','si013724','l1 lmd fasi','f','2007-09-05'),
('delohim','sulemani','eclat-gabriella','si089234','l1 lmd fasi','f','2006-06-05'),
('teto','filoreto','christian','si756122','l1 lmd fasi','m','2007-04-21'),
('mbuyu','ilunga','franck','si431290','l1 lmd fasi','m','2003-12-12'),
('nguimbi','lolo','divine','si561908','l1 lmd fasi','f','2006-06-16'),
('madidi','imunga','toussaint','si756041','l1 lmd fasi','m','2007-03-28'),
('kalala','odia','princesse','si879525','l1 lmd fasi','f','2006-11-04'),
('musadi','kadima','theodora','si091234','l1 lmd fasi','f','2007-01-20'),
('longo','longo','ainsi','si103002','l1 lmd fasi','m','2005-03-03'),
('kipaka',null,'michel','si750192','l1 lmd fasi','m','2007-01-12'),
('tshikalu','matshi','fanaim','ae432678','l1 lmd fase','f','2006-05-23'),
('katende','lumbu','emmanuel','ae435671','l1 lmd fase','m','2006-06-24'),
('masenge','lumbala','naomie','ae354629','l1 lmd fase','f','2007-02-26'),
('dikonga',null,'joseph','ae201367','l1 lmd fase','m','2005-09-04'),
('bingi','fatouma','divina','md456370','g0 medecine','f','2007-07-14'),
('kengo',null,'olive','md425009','g0 medecine','f','2006-09-15'),
('kongolo','mwamba','elisee','md675813','g0 medecine','m','2005-11-05'),
('azima','bembida','hope','dr600912','l1 lmd droit','f','2007-12-24'),
('ramazani',null,'jacques','dr231098','l1 lmd droit','m','2004-06-04'),
('nyangila',null,'jacques','th001234','l1 lmd theologie','m','2001-06-29'),
('ndualu',null,'chillo','th351673','l1 lmd theologie','m','2001-10-21')

