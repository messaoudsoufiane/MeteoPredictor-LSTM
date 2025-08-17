import ee

# Initialiser l'API Google Earth Engine
ee.Initialize()
try:
    ee.Initialize()
    print("Google Earth Engine initialisé avec succès !")


# Définir la zone d'intérêt (Casablanca par exemple)
    roi = ee.Geometry.Point([-1.911389, 34.686667])  # Longitude, Latitude

    # Définir la période
    start_date = '2023-01-01'
    end_date = '2025-12-31'

    # Charger la collection d'images Sentinel-2
    collection = ee.ImageCollection('COPERNICUS/S2') \
        .filterBounds(roi) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))  # Filtrer les images avec moins de 10% de nuages

    # Sélectionner une image (première de la collection)
    image = collection.first()

    # Visualisation (pour vérifier dans la console GEE)
    url = image.getThumbUrl({'min': 0, 'max': 3000, 'bands': ['B4', 'B3', 'B2']})
    print(f"URL pour visualisation : {url}")

    # Exporter l'image pour la télécharger
    task = ee.batch.Export.image.toDrive(
        image=image.clip(roi.buffer(10000)),  # Découpe autour de la région d'intérêt
        description='Satellite_Image',
        folder='EarthEngine',
        fileNamePrefix='casablanca_satellite',
        scale=10,  # Résolution en mètres par pixel
        region=roi.buffer(10000).bounds().getInfo()['coordinates']  # Zone d'intérêt
    )
    task.start()
    print("Exportation lancée. Vérifie Google Drive.")
except ee.EEException as e:
    print("Erreur lors de l'initialisation :", str(e))
    print("Assurez-vous d'avoir activé votre compte sur https://earthengine.google.com/signup/")