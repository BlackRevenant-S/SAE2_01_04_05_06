import sqlalchemy as sa

user = "postgres"
password = "vitrygtr"
host = "localhost"
port = 5432
dbname = "postgres"

url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
engine = sa.create_engine(url)

try:
    with engine.connect() as conn:
        result = conn.execute("SELECT version();")
        print("Connexion OK :", result.fetchone())
except Exception as e:
    print("Erreur :", e)