# 🌦️ Weather Prediction with LSTM - Casablanca Project

Projet académique de prédiction météorologique basé sur l’intelligence artificielle. Ce projet combine la collecte de données météo, le traitement de séries temporelles, des images satellites, l’entraînement d’un modèle LSTM multi-sorties, et la prédiction de plusieurs variables climatiques.

## 📚 Sommaire

- [🔍 Objectif du projet](#-objectif-du-projet)
- [🛠️ Technologies utilisées](#-technologies-utilisées)
- [📥 Collecte des données](#-collecte-des-données)
- [🧹 Prétraitement](#-prétraitement)
- [🧠 Modélisation LSTM](#-modélisation-lstm)
- [📊 Visualisation & Résultats](#-visualisation--résultats)
- [🧪 Prédictions sur de nouvelles données](#-prédictions-sur-de-nouvelles-données)
- [🗃️ Base de données MongoDB](#️-base-de-données-mongodb)
- [🛰️ Intégration Satellite (GEE)](#️-intégration-satellite-gee)
- [🚀 Lancer le projet](#-lancer-le-projet)
- [📄 Licence](#-licence)

---

## 🔍 Objectif du projet

Prédire les conditions météorologiques quotidiennes à Casablanca (et potentiellement d'autres villes) à partir de 15 jours d'historique météo :
- Température maximale (`tmax`)
- Température minimale (`tmin`)
- Précipitations (`prcp`)
- Vitesse du vent (`wspd`)
- Pression atmosphérique (`pres`)

---

## 🛠️ Technologies utilisées

- **Python** 3.x
- **Meteostat** pour les données météo historiques
- **Pandas / NumPy** pour le traitement des données
- **TensorFlow / Keras** pour le modèle LSTM
- **Matplotlib** pour les visualisations
- **MongoDB** pour le stockage structuré
- **Google Earth Engine (GEE)** pour les images satellites Sentinel-2
- **Joblib** pour la persistance des scalers
- **CSV** pour l'import/export de jeux de données

---

## 📥 Collecte des données

- Les données météorologiques sont extraites de l'API `Meteostat` pour Casablanca entre 2023-10-04 et 2023-12-19.
- Un script `collect_data.py` génère un fichier `vvv.csv` contenant :
  - tmin, tmax, prcp, wspd, pres, wdir, etc.

---

## 🧹 Prétraitement

- Suppression des colonnes non utiles (`tavg`, `tsun`, `snow`, etc.).
- Remplissage des valeurs manquantes avec la moyenne des jours voisins.
- Normalisation via `MinMaxScaler`.
- Encodage one-hot pour les noms de ville (si multiville).

---

## 🧠 Modélisation LSTM

- Réseau neuronal LSTM à 2 couches avec `Dropout`.
- Données séquentielles de 15 jours → 5 sorties météo.
- Entraînement sur `X_train` / `y_train`, évaluation sur `X_test`.
- Sauvegarde du modèle dans `multi_output_lstm_model2.h5`.

---

## 📊 Visualisation & Résultats

- Affichage de la perte (`loss` & `val_loss`) pendant l'entraînement.
- Graphiques comparatifs **valeurs réelles vs. prédictions** pour chaque variable cible.
- Évaluation : MSE et MAE sur données test.

---

## 🧪 Prédictions sur de nouvelles données

- Script `test.py` :
  - Charge de nouvelles données (ex : `vvv.csv`)
  - Génère des séquences
  - Effectue la prédiction via le modèle entraîné
  - Sauvegarde les résultats dans `predictions.csv`

---
