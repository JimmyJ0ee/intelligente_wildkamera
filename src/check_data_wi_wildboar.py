import os
import csv
import shutil
import os
import pandas as pd


def count_images_and_csv_entries(image_folder, csv_file):
    # Liste der Bildnamen im Ordner abrufen
    image_names = set(os.listdir(image_folder))
    # print(image_names)
    # Zähler initialisieren
    images_in_csv = 0

    # CSV-Datei lesen und Einträge zählen
    with open(csv_file, mode="r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            image_id = str(row["image_id"]) + ".JPG"
            if image_id in image_names:
                images_in_csv += 1
    return images_in_csv


def split_images(image_folder, csv_file):
    destination_folder = "./../.data/wi_wild_boar/images_w_label"
    zaehler = 0
    # CSV-Datei lesen und Einträge zählen
    df = pd.read_csv(csv_file)
    filtered_df = df[df["bounding_boxes"].notna() & (df["bounding_boxes"] != "")]
    image_ids = filtered_df.image_id.to_list()
    # print(len(image_ids), image_ids)
    for filename in os.listdir(image_folder):
        if filename[:-4] in image_ids:
            source_file = os.path.join(image_folder, filename)
            destination_file = os.path.join(destination_folder, filename)
            shutil.move(source_file, destination_file)
            print(f"{filename} wurde verschoben.")
            zaehler += 1
    print(zaehler)


# Beispielverwendung
image_folder = "./../.data/wi_wild_boar/images"
csv_file = "./../.data/wi_wild_boar/labels/images_2004096.csv"

images_in_csv = count_images_and_csv_entries(image_folder, csv_file)
split_images(image_folder, csv_file)

print(
    f"Anzahl der Bilder in der CSV: {images_in_csv} (Bilder ohne label und Duplikate noch mit drin)"
)
