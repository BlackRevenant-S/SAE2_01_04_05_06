#####################################################################
# IMPORTATION DES MODULES
#####################################################################

from flask import Flask, render_template, request
import numpy as np
import folium


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
# CONTROLEUR : LIAISON AVEC LA BASE DE DONNEES
#####################################################################



if __name__ == '__main__':
    app.run(debug=True)