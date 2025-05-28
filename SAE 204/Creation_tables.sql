/*create table region (
	code_region varchar(255) PRIMARY KEY,
	libelle_region varchar(255)
);*/

/*create table departement (
	code_departement varchar(255) primary key,
	libelle_departement varchar(255),
	code_region varchar(255),
	foreign key(code_region) references region(code_region)
);*/

/*create table cours_eau (
	code_cours_eau varchar(255) primary key,
	libelle_cours_eau varchar(255)
);*/

/*create table commune (
	code_commune varchar(255) primary key,
	libelle_commune varchar(255),
	code_departement varchar(255),
	foreign key(code_departement) references departement(code_departement)
);*/

/*create table station (
	code_station varchar(255) primary key,
	libelle_station varchar(255),
	longitude float,
	latitude float,
	altitude float,
	code_cours_eau varchar(255),
	code_commune varchar(255),
	foreign key(code_cours_eau) references cours_eau(code_cours_eau),
	foreign key(code_commune) references commune(code_commune)
);*/
