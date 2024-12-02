import os
import os
import pandas as pd
import re
from tqdm import tqdm

from wi_to_yolo_format import rename_files_in_directory


def count_images_and_csv_entries(image_folder, csv_file):
    """
    Vergleicht Bildernamen mit Namen aus Spalte 'location'.
    Löst Problem, dass nur ein Teil oder gar kein Bild in der Spalte "image_id" zu finden ist.
    """

    image_names = set(os.listdir(image_folder))
    images_in_csv = 0

    # CSV-Datei lesen und Einträge zählen
    df = pd.read_csv(csv_file)

    col_location = df["location"].tolist()
    # Anzahl der Übereinstimmungen zählen
    images_in_csv = sum(
        1
        for name in tqdm(col_location)
        if any(image_name in name for image_name in image_names)
    )

    # for image_name in image_names:
    #     for name in col_location:
    #         if image_name in name:
    #             images_in_csv += 1

    print(
        f"Anzahl der Bilder in der CSV: {images_in_csv} (Bilder ohne label und Duplikate noch mit drin)"
    )


try:
    rename_files_in_directory(".data/data_deer_wild_boar_yolo/data/validation/images")
    rename_files_in_directory(".data/data_deer_wild_boar_yolo/data/validation/labels")
    rename_files_in_directory(".data/data_deer_wild_boar_yolo/data/test/images")
    rename_files_in_directory(".data/data_deer_wild_boar_yolo/data/test/labels")
    rename_files_in_directory(".data/data_deer_wild_boar_yolo/data/train/images")
    rename_files_in_directory(".data/data_deer_wild_boar_yolo/data/train/labels")
except FileExistsError as e:
    print(e)
except WindowsError as e:
    print(e)
