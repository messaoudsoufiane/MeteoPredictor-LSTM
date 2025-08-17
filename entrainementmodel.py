import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt
import joblib  # Pour sauvegarder les scalers

# Charger le fichier CSV
file_path = "casa.csv"  # Remplace par ton fichier
data = pd.read_csv(file_path, parse_dates=["date"])

# Trier les données par date
data = data.sort_values(by="date")

# Ajouter la colonne 'ville' si nécessaire avec encodage one-hot
if "ville" in data.columns:
    data = pd.get_dummies(data, columns=["ville"])

# Définir les colonnes d'entrée (features) et de sortie (targets)
features = ["tmax", "tmin", "wspd", "prcp", "pres", "wdir"]  # Inclure tmax dans les entrées
if "ville" in data.columns:
    features += [col for col in data.columns if col.startswith("ville_")]  # Ajouter les colonnes encodées pour 'ville'

targets = ["tmax", "tmin", "prcp", "wspd", "pres"]  # Variables à prédire (multi-output)

# Créer des scalers séparés pour les features et les targets
scaler_features = MinMaxScaler()
scaler_targets = MinMaxScaler()

# Ajuster et transformer les features
scaled_features = scaler_features.fit_transform(data[features])

# Ajuster et transformer les targets
scaled_targets = scaler_targets.fit_transform(data[targets])

# Combiner les données normalisées
scaled_data = np.hstack((scaled_features, scaled_targets))

# Sauvegarder les scalers pour les utiliser pendant le test
joblib.dump(scaler_features, "scaler_features2.pkl")
joblib.dump(scaler_targets, "scaler_targets2.pkl")
print("Scalers sauvegardés avec succès.")

# Convertir les données en séquences pour LSTM
def create_sequences_multi_output(data, sequence_length):
    X, y = [], []
    for i in range(len(data) - sequence_length):
        X.append(data[i:i + sequence_length, :len(features)])  # Séquences des features
        y.append(data[i + sequence_length, len(features):])  # Multi-output targets
    return np.array(X), np.array(y)

sequence_length = 15  # Utiliser 15 jours précédents pour prédire le prochain jour
X, y = create_sequences_multi_output(scaled_data, sequence_length)

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Forme des données d'entraînement : {X_train.shape}, {y_train.shape}")
print(f"Forme des données de test : {X_test.shape}, {y_test.shape}")

# Construire le modèle LSTM
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
    Dropout(0.2),
    LSTM(64, return_sequences=False),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(y_train.shape[1])  # Sortie multi-output (une sortie pour chaque target)
])

# Compiler le modèle
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Afficher le résumé du modèle
model.summary()

# Entraîner le modèle
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=100,
    batch_size=32,
    verbose=1
)

# Visualiser l'évolution de la perte
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Perte (entraînement)')
plt.plot(history.history['val_loss'], label='Perte (validation)')
plt.xlabel('Épochs')
plt.ylabel('Perte')
plt.legend()
plt.title('Évolution de la perte')
plt.show()

# Évaluer le modèle sur l'ensemble de test
loss, mae = model.evaluate(X_test, y_test, verbose=0)
print(f"Perte (MSE) sur l'ensemble de test : {loss}")
print(f"Erreur absolue moyenne (MAE) : {mae}")

# Prédire les valeurs sur l'ensemble de test
y_pred = model.predict(X_test)

# Inverser la normalisation pour interpréter les résultats
def inverse_transform(scaler, data, num_features):
    temp = np.zeros((len(data), num_features))
    temp[:, -data.shape[1]:] = data
    return scaler.inverse_transform(temp)[:, -data.shape[1]:]

y_test_rescaled = inverse_transform(scaler_targets, y_test, len(targets))
y_pred_rescaled = inverse_transform(scaler_targets, y_pred, len(targets))

# Visualiser les prédictions pour chaque cible
target_names = ["Température maximale (tmax)", "Température minimale (tmin)", "Précipitations (prcp)", "Vitesse du vent (wspd)", "Pression (pres)"]
for i, target in enumerate(target_names):
    plt.figure(figsize=(10, 6))
    plt.plot(y_test_rescaled[:, i], label=f"Valeurs réelles ({target})")
    plt.plot(y_pred_rescaled[:, i], label=f"Prédictions ({target})")
    plt.legend()
    plt.title(f"Prédictions vs Valeurs réelles pour {target}")
    plt.xlabel("Exemples")
    plt.ylabel(target)
    plt.show()

# Sauvegarder le modèle
model.save("multi_output_lstm_model2.h5")
print("Modèle sauvegardé sous 'multi_output_lstm_model.h5'")
