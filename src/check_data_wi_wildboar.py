import os
import csv
import shutil
import os
import pandas as pd
import re
from tqdm import tqdm


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


def split_images(
    image_folder,
    csv_file,
    destination_folder_w_label,
    destination_folder_wo_label,
    animal,
):
    """Trennt Bilder ohne Label von Bildern mit Label.

    Merke: Implementierung macht keinen Sinn, wenn Bilder ohne BB hier nicht mit gelöscht werden.
    Falls das weiterhin so bleibt, sollte das shuttil.copy und die Verzweigung aufgelöst werden,
    und Bilder ohne Label gelöscht werden.
    """

    zaehler = 0
    os.makedirs(destination_folder_w_label, exist_ok=True)
    os.makedirs(destination_folder_wo_label, exist_ok=True)

    # Label lesen + Duplikate löschen
    df = pd.read_csv(csv_file)
    df_animal = df.loc[df["common_name"].isin(animal)]
    print(df.shape)
    # Doppelte Vorkommen sind evtl. 1x falsch klassifiziert. Löschen sichert Qualität des Datensatzes.
    wo_duplicates = df_animal["location"].drop_duplicates()
    col_location = wo_duplicates.tolist()
    print(len(col_location))

    image_names = set(os.listdir(image_folder))

    for name in tqdm(col_location):
        muster = r"[^/]+$"
        dateiname = re.search(muster, name).group()
        if dateiname in image_names:
            source_file = os.path.join(image_folder, dateiname)
            destination_file = os.path.join(destination_folder_w_label, dateiname)
            try:
                shutil.copy(source_file, destination_file)

            except FileNotFoundError as e:
                print(e, dateiname)
            zaehler += 1
        else:
            source_file = os.path.join(image_folder, dateiname)
            destination_file = os.path.join(destination_folder_wo_label, dateiname)
            try:
                shutil.copy(source_file, destination_file)
            except FileNotFoundError as e:
                print(e, dateiname)
    print(
        f"Anzahl der Bilder in der CSV: {zaehler} (Bilder ohne label und Duplikate gelöscht)"
    )


# Pfade
image_folder = ".data/not_used/wi_badger/images"
csv_file = ".contrib/images_2004096.csv"
destination_folder_w_label = ".data/not_used/wi_badger/images_w_label"
destination_folder_wo_label = ".data/not_used/wi_badger/images_wo_label"
animal = ("Eurasian Badger",)  # Name des Tiers in der Spalte "common_name"


# images_in_csv = count_images_and_csv_entries(image_folder, csv_file)
split_images(
    image_folder,
    csv_file,
    destination_folder_w_label,
    destination_folder_wo_label,
    animal,
)
