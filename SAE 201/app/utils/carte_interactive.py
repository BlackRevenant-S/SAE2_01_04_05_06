import folium

# Créer une carte sans fond (pas de tuiles)
carte = folium.Map(
    location=[46.5, 2.2],  # Centre de la France
    zoom_start=6,
    tiles=None  # Aucune tuile (carte blanche)
)

# Optionnel : ajouter une forme ou un marqueur
folium.Marker([48.8566, 2.3522], popup="Paris").add_to(carte)

carte.save("carte.html")