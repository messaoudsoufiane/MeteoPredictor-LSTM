import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import joblib
from tensorflow.keras.losses import MeanSquaredError

# Charger le modèle
model = load_model("multi_output_lstm_model2.h5", custom_objects={"mse": MeanSquaredError()})
print("Modèle chargé avec succès.")

# Charger les scalers sauvegardés
scaler_features = joblib.load("scaler_features2.pkl")
scaler_targets = joblib.load("scaler_targets2.pkl")
print("Scalers des features et targets chargés avec succès.")

# Charger les nouvelles données
new_data_path = "vvv.csv"  # Remplace par ton fichier contenant les nouvelles données
new_data = pd.read_csv(new_data_path, parse_dates=["date"])

# Trier les données par date
new_data = new_data.sort_values(by="date")

# Vérifier la présence de la colonne `ville` et encoder si nécessaire
if "ville" in new_data.columns:
    new_data = pd.get_dummies(new_data, columns=["ville"])

# Définir les colonnes d'entrée (features)
features = ["tmax", "tmin", "wspd", "prcp", "pres", "wdir"]
if "ville" in new_data.columns:
    features += [col for col in new_data.columns if col.startswith("ville_")]

# Vérifier les colonnes disponibles et les valeurs manquantes
print("Colonnes disponibles :", new_data.columns)
print("Valeurs manquantes :", new_data[features].isnull().sum())

# Remplacer les valeurs manquantes par 0
new_data[features] = new_data[features].fillna(0)

# Normaliser les nouvelles données en utilisant le scaler des features
scaled_features = scaler_features.transform(new_data[features])

# Générer les séquences pour les nouvelles données
def create_sequences_for_test(data, sequence_length):
    X = []
    for i in range(len(data) - sequence_length + 1):
        X.append(data[i:i + sequence_length])
    return np.array(X)

sequence_length = 15  # Doit correspondre à celui utilisé lors de l'entraînement
X_test_new = create_sequences_for_test(scaled_features, sequence_length)

# Vérifier la forme des données pour la prédiction
print(f"Forme des nouvelles données pour la prédiction : {X_test_new.shape}")

# Si les données sont suffisantes pour créer des séquences
if X_test_new.shape[0] > 0:
    # Effectuer les prédictions
    y_pred_scaled = model.predict(X_test_new)

    # Inverser la normalisation des targets
    def inverse_transform_targets(scaler, predictions):
        return scaler.inverse_transform(predictions)

    y_pred = inverse_transform_targets(scaler_targets, y_pred_scaled)

    # Définir les colonnes des prédictions
    predicted_columns = ["tmax", "tmin", "prcp", "wspd", "pres"]
    predictions_df = pd.DataFrame(y_pred, columns=predicted_columns)

    # Afficher les prédictions
    print("Prédictions :")
    print(predictions_df)

    # Sauvegarder les prédictions dans un fichier CSV
    predictions_df.to_csv("predictions.csv", index=False)
    print("Prédictions sauvegardées dans le fichier 'predictions.csv'.")
else:
    print("Pas assez de données pour effectuer des prédictions.")
