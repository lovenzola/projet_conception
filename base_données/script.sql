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

insert into etudiants (nom,postnom,prenom,matricule,promotion)
values ('tshikalu','masthi','fanaim','ae324155','l1 lmd fase'),
('katende','lumbu','emmanuel',)