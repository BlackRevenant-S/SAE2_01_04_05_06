#####################################################################
# IMPORTATION DES MODULES
#####################################################################

from flask import Flask, render_template, request
import numpy as np


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
def accueil():
    # Affichage du template
    return render_template('index.html')