import folium
import requests
from folium import MacroElement
from jinja2 import Template
import sqlalchemy as sa 
import pandas as pd



#Télécharger le GeoJSON des régions françaises qui sont sur un github
url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson"
geojson_data = requests.get(url).json()

##########################################
#point station
##########################################

user = "postgres"
password = "vitrygtr"
host = "localhost"
port = 5432
dbname = "postgres"


url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
engine = sa.create_engine(url)

# 2. Créer une carte blanche centrée sur la France
carte = folium.Map(location=[46.5, 2.2], zoom_start=6.2, tiles=None)

query = "SELECT libelle_station, latitude, longitude FROM station"
df = pd.read_sql(query, engine)

for _, row in df.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        tooltip=row["libelle_station"]
    ).add_to(carte)



# Dictionnaire avec une couleur par région 
couleurs_regions = {
    "Auvergne-Rhône-Alpes": "#e41a1c",
    "Bourgogne-Franche-Comté": "#377eb8",
    "Bretagne": "#4daf4a",
    "Centre-Val de Loire": "#984ea3",
    "Corse": "#ff7f00",
    "Grand Est": "#ffff33",
    "Hauts-de-France": "#a65628",
    "Île-de-France": "#f781bf",
    "Normandie": "#999999",
    "Nouvelle-Aquitaine": "#66c2a5",
    "Occitanie": "#fc8d62",
    "Pays de la Loire": "#8da0cb",
    "Provence-Alpes-Côte d'Azur": "#e78ac3",
}

# 3. Créer la couche GeoJSON avec une couleur différente par région
def style_function(feature):
    region_nom = feature['properties']['nom']
    couleur = couleurs_regions.get(region_nom, "white")  # Blanc si la région n'est pas dans le dict
    return {
        "fillColor": couleur,
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.8,
    }

geojson_layer = folium.GeoJson(
    geojson_data,
    name="régions",
    style_function=style_function,
    highlight_function=lambda feature: {
        "fillOpacity": 0.7,
        "color": "black",
        "weight": 2,
    },
    tooltip=folium.GeoJsonTooltip(fields=["nom"], aliases=["Région :"]),
)

# 4. Ajouter le JS pour le zoom au clic (comme dans ton code)
zoom_js = MacroElement()
zoom_js._template = Template("""
{% macro script(this, kwargs) %}
    {{this._parent.get_name()}}.eachLayer(function(layer) {
        layer.on('click', function(e) {
            {{this._parent._parent.get_name()}}.fitBounds(e.target.getBounds());
        });
    });
{% endmacro %}
""")
geojson_layer.add_child(zoom_js)

geojson_layer.add_to(carte)

# Télécharger le GeoJSON des départements (inchangé)
url_dep = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson"
geojson_dep = requests.get(url_dep).json()

geojson_layer_dep = folium.GeoJson(
    geojson_dep,
    name="départements",
    style_function=lambda feature: {
        "fillColor": "none",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0,
    },
    tooltip=folium.GeoJsonTooltip(fields=["nom"], aliases=["Département :"]),
)
geojson_layer_dep.add_to(carte)

carte.save("SAE 201/app/templates/carte.html")



with open("SAE 201/app/templates/carte.html", "a") as f:
  f.write("""<style>
    path.leaflet-interactive:focus {
        outline: none;
    }
    svg path {
        outline: none;
        stroke-linecap: round;
    }
</style>""")
  


  
with open("SAE 201/app/templates/carte.html", "a") as g:
   g.write("""<script>
function onMarkerClick(nom) {
    window.parent.postMessage( nom, '*');
}

// Exemple d'ajout d'un listener sur tous les markers (Leaflet)
setTimeout(() => {
  for(let key in window) {
    if(window[key] instanceof L.Marker) {
      window[key].on('click', onMarkerClick());
    }
  }
}, 500);
</script>""")

