# import numpy as np
# import cv2
# from PIL import Image
# import matplotlib.pyplot as plt
# import os
# from ultralytics import YOLO

# print(os.getcwd())
# model = YOLO(
#     "./../runs/detect_yolo8n_wild_boar+deer/yolov8n_deer_and_wild_boar2024-11-20 14_38_43.108048.pt"
# )

# path_test = "C:/Users/Z0127829/OneDrive - ZF Friedrichshafen AG/Desktop/Arbeit/Studienarbeit/intelligente_wildkamera/.data/evaluation/video/no_deer/IMAG0030.AVI"
# results = model.predict(source=path_test, save=True, stream=True)
import re

# Adresse
adresse = "gs://145625598251_2004096_618_tfwp__main/deployment/2137488/68263bf0-516c-43f9-8a30-a11d8d7e8006.JPG"

# Regulärer Ausdruck zur Extraktion des Dateinamens mit Endung
muster = r"[^/]+$"
dateiname = re.search(muster, adresse).group()

print(dateiname)
print(f"{dateiname[:-4]}.txt")
