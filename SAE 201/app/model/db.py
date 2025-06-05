import pandas as pd
import sqlalchemy as sa
import psycopg2

# Connexion à la base de données statique PostgreSQL
def connect_db():
    return sa.create_engine("postgresql+psycopg2://postgres:vitrygtr@localhost:5432/postgres")

# Champ de recherche de stations. On récupère l'ID récupéré par le controleur dans le HTML
def get_station_list(saisie_utilisateur):
    conn = connect_db()
    query = f"SELECT station.code_station, station.libelle_station, commune.libelle_commune, departement.libelle_departement \
    FROM station \
    JOIN commune on station.code_commune = commune.code_commune \
    JOIN departement on commune.code_departement = departement.code_departement \
    JOIN region on departement.code_region = region.code_region \
    JOIN cours_eau on station.code_cours_eau = cours_eau.code_cours_eau \
    WHERE libelle_station = '%{saisie_utilisateur}%'"
    
    station_list = pd.read_sql_query(query, conn)
    return station_list

# Fitrage des recherches par région
def get_filter_by_region(code_region):
    conn = connect_db()
    query = f"SELECT station.code_station, station.libelle_station, commune.libelle_commune, departement.libelle_departement \
    FROM station \
    JOIN commune on station.code_commune = commune.code_commune \
    JOIN departement on commune.code_departement = departement.code_departement \
    JOIN region on departement.code_region = region.code_region \
    JOIN cours_eau on station.code_cours_eau = cours_eau.code_cours_eau \
    WHERE code_region = {code_region}"

    filter_by_region = pd.read_sql_query(query, conn)
    return filter_by_region

# Filtrage des recherches par département
def get_filter_by_department(code_departement):
    conn = connect_db()
    query = f"SELECT station.code_station, station.libelle_station, commune.libelle_commune, departement.libelle_departement \
    FROM station \
    JOIN commune on station.code_commune = commune.code_commune \
    JOIN departement on commune.code_departement = departement.code_departement \
    JOIN region on departement.code_region = region.code_region \
    JOIN cours_eau on station.code_cours_eau = cours_eau.code_cours_eau \
    WHERE code_departement = {code_departement}"

    filter_by_department = pd.read_sql_query(query, conn)
    return filter_by_department

# Filtrage des recherches par commune
def get_filter_by_commune(code_commune):
    conn = connect_db()
    query = f"SELECT station.code_station, station.libelle_station, commune.libelle_commune, departement.libelle_departement \
    FROM station \
    JOIN commune on station.code_commune = commune.code_commune \
    JOIN departement on commune.code_departement = departement.code_departement \
    JOIN region on departement.code_region = region.code_region \
    JOIN cours_eau on station.code_cours_eau = cours_eau.code_cours_eau \
    WHERE code_commune = {code_commune}"

    filter_by_commune = pd.read_sql_query(query, conn)
    return filter_by_commune

# Filtrage des recherches par cours d'eau
def get_filter_by_watercourse(code_cours_eau):
    conn = connect_db()
    query = f"SELECT station.code_station, station.libelle_station, commune.libelle_commune, departement.libelle_departement \
    FROM station \
    JOIN commune on station.code_commune = commune.code_commune \
    JOIN departement on commune.code_departement = departement.code_departement \
    JOIN region on departement.code_region = region.code_region \
    JOIN cours_eau on station.code_cours_eau = cours_eau.code_cours_eau \
    WHERE code_cours_eau = {code_cours_eau}"

    filter_by_watercourse = pd.read_sql_query(query, conn)
    return filter_by_watercourse

# Page détaillée de la station
def get_station_details(code_station):
    conn = connect_db()
    query = f"SELECT station.code_station, station.libelle_station, station.longitude, station.latitude, station.altitude, commune.code_commune, \
    commune.libelle_commune, departement.libelle_departement, region.code_region, region.libelle_region \
    FROM station \
    JOIN commune on station.code_commune = commune.code_commune \
    JOIN departement on commune.code_departement = departement.code_departement \
    JOIN region on departement.code_region = region.code_region \
    JOIN cours_eau on station.code_cours_eau = cours_eau.code_cours_eau \
    WHERE code_station = {code_station}"

    station_details = pd.read_sql_query(query, conn)
    return station_details