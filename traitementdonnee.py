import pandas as pd
import pandas as pd
import numpy as np

# Charger les données
file_path = "vvv.csv"  # Remplace par ton fichier
data = pd.read_csv(file_path)

# Supprimer les colonnes inutiles
columns_to_drop = ["tavg", "snow", "wpgt", "tsun"]
data = data.drop(columns=columns_to_drop)

# Remplacer les valeurs manquantes de 'prcp' par la moyenne des voisins
def fill_with_neighbors_mean(column):
    for i in range(len(column)):
        if pd.isna(column[i]):
            # Trouver les voisins valides (non NaN)
            neighbors = []
            if i > 0 and not pd.isna(column[i - 1]):
                neighbors.append(column[i - 1])
            if i < len(column) - 1 and not pd.isna(column[i + 1]):
                neighbors.append(column[i + 1])
            # Calculer la moyenne des voisins et remplacer
            if neighbors:
                column[i] = np.mean(neighbors)
    return column

data["prcp"] = fill_with_neighbors_mean(data["prcp"].values)

# Sauvegarder les données nettoyées
output_file = "vvv.csv"
data.to_csv(output_file, index=False)

print(f"Données nettoyées sauvegardées dans le fichier : {output_file}")

# Charger le fichier CSV
file_path = "vvv.csv"  # Remplace par le chemin de ton fichier
data = pd.read_csv(file_path)

# Vérifier le nombre de valeurs nulles par colonne
null_counts = data.isnull().sum()


# Afficher les résultats
print("Valeurs nulles par colonne :")
print(null_counts)

# Vérifier le total des valeurs nulles dans tout le DataFrame
total_nulls = data.isnull().sum().sum()
print(f"Nombre total de valeurs nulles dans le fichier : {total_nulls}")
