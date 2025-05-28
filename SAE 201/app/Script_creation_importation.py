import pandas as pd, sqlalchemy, json, requests, psycopg2

# Remplacez l'URL par l'endpoint de l'API d'Hubeau pour les températures des cours d'eau
url = "https://hubeau.eaufrance.fr/api/v1/temperature/station"

# Faire une requête GET à l'API
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:

    # Connect to an existing database
    conn = psycopg2.connect("dbname=test user=postgres")

    # Open a cursor to perform database operations
    cur = conn.cursor()


    # Execute a command: this creates a new table
    cur.execute("""create table region IF NOT EXISTS (
	code_region varchar(255) PRIMARY KEY,
	libelle_region varchar(255)
    );

    create table departement IF NOT EXISTS (
	code_departement varchar(255) primary key,
	libelle_departement varchar(255),
	code_region varchar(255),
	foreign key(code_region) references region(code_region)
    );

    create table cours_eau IF NOT EXISTS (
	code_cours_eau varchar(255) primary key,
	libelle_cours_eau varchar(255)
    );

    create table commune IF NOT EXISTS (
	code_commune varchar(255) primary key,
	libelle_commune varchar(255),
	code_departement varchar(255),
	foreign key(code_departement) references departement(code_departement)
    );

    create table station IF NOT EXISTS (
	code_station varchar(255) primary key,
	libelle_station varchar(255),
	longitude float,
	latitude float,
	altitude float,
	code_cours_eau varchar(255),
	code_commune varchar(255),
	foreign key(code_cours_eau) references cours_eau(code_cours_eau),
	foreign key(code_commune) references commune(code_commune)
    );""")

    # Charger les données JSON depuis la réponse de l'API
    data = response.json()["data"]

    dataframe = pd.DataFrame(data)

    # Connexion à PostgreSQL
    conn_db = sqlalchemy.create_engine("postgresql+psycopg2://postgres:vitrygtr@localhost:5432/postgres")

    # Extraction et importation des attributs pour la table region tout en supprimant les données en doublons
    regions = dataframe[["code_region", "libelle_region"]].drop_duplicates().dropna()
    regions.to_sql("region", conn_db, if_exists="append", index=False)

    # Extraction et importation des attributs pour la table departement tout en supprimant les données en doublons
    departements = dataframe[["code_departement", "libelle_departement", "code_region"]].drop_duplicates().dropna()
    departements.to_sql("departement", conn_db, if_exists="append", index=False)

    # Extraction et importation des attributs pour la table commune tout en supprimant les données en doublons
    communes = dataframe[["code_commune", "libelle_commune", "code_departement"]].drop_duplicates().dropna()
    communes.to_sql("commune", conn_db, if_exists="append", index=False)

    # Extraction et importation* des attributs pour la table cours_eau tout en supprimant les données en doublons
    cours_eau = dataframe[["code_cours_eau", "libelle_cours_eau"]].drop_duplicates().dropna()
    cours_eau.to_sql("cours_eau", conn_db, if_exists="append", index=False)

    # Extraction et importation des attributs pour la table station tout en supprimant les données en doublons
    stations = dataframe[[
        "code_station", "libelle_station",
        "longitude", "latitude", "altitude", "code_cours_eau", "code_commune"
    ]].drop_duplicates().dropna()

    # Filtre les stations qui sont contenues dans la table cours_eau (qui existent)
    stations = stations[stations["code_cours_eau"].isin(cours_eau["code_cours_eau"])]
    stations = stations[stations["code_commune"].isin(communes["code_commune"])]
    # Importation*
    stations.to_sql("station", conn_db, if_exists="append", index=False)

    # Afficher les DataFrames pour vérifier les données
    print("Régions:")
    print(regions)
    print("\nDépartements:")
    print(departements)
    print("\nCommunes:")
    print(communes)
    print("\nCours d'eau:")
    print(cours_eau)
    print("\nStations:")
    print(stations)
else:
    print(f"Erreur lors de la requête à l'API: {response.status_code}")