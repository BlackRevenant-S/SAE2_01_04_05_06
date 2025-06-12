#####################################################################
# IMPORTATION DES MODULES
#####################################################################

from flask import Flask, render_template, request
import numpy as np, folium, json, requests, pandas as pd

#####################################################################
# CONFIGURATION
#####################################################################


# Déclaration d'application Flask
app = Flask(__name__,
            static_folder='templates/static')

#####################################################################
# CONTROLEUR : ROUTES VERS LES VUES
#####################################################################

#### LIENS HTML

# Route pour la page d'accueil
@app.route('/')
def index():
    # Affichage du template
    return render_template('index.html')

#####################################################################
# CONTROLEUR : IMPORTATION DES DONNEES DE L'API
#####################################################################

# Remplacez l'URL par l'endpoint de l'API d'Hubeau pour les températures des cours d'eau
url = "https://hubeau.eaufrance.fr/api/v1/temperature/station"

# Faire une requête GET à l'API
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Charger les données JSON depuis la réponse de l'API
    data = response.json()["data"]

    dataframe = pd.DataFrame(data)

#####################################################################
# CONTROLEUR : LIAISON AVEC LA BASE DE DONNEES
#####################################################################



if __name__ == '__main__':
    app.run(debug=True)