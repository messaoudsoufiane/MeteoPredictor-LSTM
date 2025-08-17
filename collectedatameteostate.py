from meteostat import Point, Daily
from datetime import datetime
import pandas as pd

# Liste des villes avec leurs coordonnées
cities = {
    "Casa": {"latitude": 33.63096279449563, "longitude": -7.624695714863305, "elevation": 0}
}

# Définir la période d'extraction
start = datetime(2023, 10, 4)  # Date de début
end = datetime(2023, 12, 19)  # Date de fin

# DataFrame pour stocker toutes les données
all_data = pd.DataFrame()

# Extraire les données pour chaque ville
for city, coords in cities.items():
    location = Point(coords["latitude"], coords["longitude"], coords["elevation"])
    data = Daily(location, start, end).fetch()  # Extraire les données
    all_data = pd.concat([all_data, data])  # Combiner les données

# Réorganiser les colonnes si nécessaire
all_data.reset_index(inplace=True)
all_data = all_data.rename(columns={"time": "date"})  # Renommer la colonne de date

# Enregistrer les données dans un fichier CSV
output_file = "vvv.csv"
all_data.to_csv(output_file, index=False)

print(f"Données météorologiques sauvegardées dans le fichier : {output_file}")
