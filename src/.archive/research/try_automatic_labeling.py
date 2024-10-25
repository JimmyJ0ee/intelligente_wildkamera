# import torch

# # Lade das vortrainierte YOLOv5-Modell
# model = torch.hub.load("ultralytics/yolov5", "yolov5s")

# # Pfad zu den Bildern
# img_dir = "./data/data/img/no_deer/"

# # Erkenne Objekte in den Bildern
# results = model(img_dir)

# # Speichere die Ergebnisse
# results.save()

import os

img_dir = r"C:\Users\Z0127829\OneDrive - ZF Friedrichshafen AG\Desktop\Arbeit\Studienarbeit\intelligente_wildkamera\data\data\img\no_deer"
os.chmod(img_dir, 0o777)
# Überprüfe, ob der Pfad existiert
if os.path.exists(img_dir):
    print("Pfad existiert.")
else:
    print("Pfad existiert nicht oder keine Berechtigung.")

# Beispiel für das Laden eines Bildes
from PIL import Image

try:
    img = Image.open(img_dir)
    img.show()
except PermissionError as e:
    print(f"Fehler: {e}")

import os
from PIL import Image

dir_path = r"C:\Users\Z0127829\OneDrive - ZF Friedrichshafen AG\Desktop\Arbeit\Studienarbeit\intelligente_wildkamera\data\data\img\no_deer"

for filename in os.listdir(dir_path):
    file_path = os.path.join(dir_path, filename)
    try:
        with Image.open(file_path) as img:
            img.verify()  # Überprüft, ob das Bild geöffnet werden kann
        print(f"{filename} erfolgreich geöffnet.")
    except Exception as e:
        print(f"Fehler beim Öffnen von {filename}: {e}")
