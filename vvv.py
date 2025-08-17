from meteostat import Point, Daily
from datetime import datetime
import pandas as pd

# Liste des villes avec leurs coordonnées
cities = {
    "Rabat": {"latitude": 34.020882, "longitude": -6.841650, "elevation": 0}
}

# Définir la période d'extraction
start = datetime(2023, 12, 14)  # Date de début
end = datetime(2023, 12, 29)  # Date de fin

# DataFrame pour stocker toutes les données
all_data = pd.DataFrame()

# Extraire les données pour chaque ville
for city, coords in cities.items():
    location = Point(coords["latitude"], coords["longitude"], coords["elevation"])
    data = Daily(location, start, end).fetch()  # Extraire les données
      # Ajouter le nom de la ville comme colonne
    all_data = pd.concat([all_data, data])  # Combiner les données

# Réorganiser les colonnes si nécessaire
all_data.reset_index(inplace=True)
all_data = all_data.rename(columns={"time": "date"})  # Renommer la colonne de date

# Enregistrer les données dans un fichier CSV
output_file = "vvv.csv"
all_data.to_csv(output_file, index=False)

print(f"Données météorologiques sauvegardées dans le fichier : {output_file}")
