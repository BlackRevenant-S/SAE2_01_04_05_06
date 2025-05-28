import folium
import requests

# Charger les données GeoJSON de la France depuis GitHub
url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson"
geojson_data = requests.get(url).json()

# Créer une carte blanche sans tuiles de fond
carte = folium.Map(location=[46.5, 2.2], zoom_start=5, tiles=None)

# Ajouter les contours en noir
folium.GeoJson(
    geojson_data,
    style_function=lambda feature: {
        "fillColor": "white",
        "color": "black",
        "weight": 1,
        "fillOpacity": 1,
    }
).add_to(carte)

# Sauvegarder la carte
carte.save("carte.html")
