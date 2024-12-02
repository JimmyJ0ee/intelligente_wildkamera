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

import os
from collections import defaultdict


import os
from collections import defaultdict
import shutil


def find_duplicates_with_common_part(directory):
    # Dictionary to store files by their common part
    common_part_dict = defaultdict(list)

    # List all files in the directory
    for root, _, files in os.walk(directory):
        for file in files:
            # Find the common part after the last underscore
            common_part = file.split("_")[-1]
            common_part_dict[common_part].append(os.path.join(root, file))

    # Find duplicates
    duplicates = {
        common_part: paths
        for common_part, paths in common_part_dict.items()
        if len(paths) > 1
    }
    print("Gelöscht:")
    for common_part, paths in duplicates.items():
        print(f"Gemeinsamer Teil: {common_part}")
        # Delete one of the duplicate files
        file_to_delete = paths[0]
        os.remove(file_to_delete)
        print(f"{common_part}")
    return duplicates


path = ".data/data_deer_wild_boar_yolo/data/train/labels"
duplicates = find_duplicates_with_common_part(path)
print("Duplikate")
for element in duplicates:
    print(element)
