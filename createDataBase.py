from pymongo import MongoClient

# Connexion au serveur MongoDB local
client = MongoClient("mongodb://localhost:27017/")

# Créer une base de données pour le projet météo
db = client["weather_project"]

# Créer une collection pour les données météorologiques
weather_collection = db["weather_data"]

print("Base de données et collection créées avec succès.")


# Exemple de document météo
sample_data = {
    "date": "2024-12-24T14:00:00Z",
    "city": "Casablanca",
    "latitude": 33.5731,
    "longitude": -7.5898,
    "temperature": {"min": 15, "max": 25, "average": 20},
    "precipitations": 0,
    "wind": {"speed": 10.5, "direction": 45},
    "pressure": 1012,
    "humidity": 65,
    "uv_index": 3,
    "weather_type": "Clear"
}

# Insérer le document dans la collection
weather_collection.insert_one(sample_data)
print("Donnée insérée avec succès.")
