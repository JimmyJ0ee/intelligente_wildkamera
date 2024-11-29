import csv
import json
import os
import random
import shutil
import re
import pandas as pd
from tqdm import tqdm
import numpy as np


def convert_to_json(data_str):
    # Überprüfen, ob der String leer ist
    if not data_str:
        return []

    # Entferne die äußeren geschweiften Klammern und teile den String in einzelne Detection-Boxen auf
    data_list = data_str.strip("{}").split('","')

    # Entferne die Anführungszeichen und wandle jede Detection-Box in ein JSON-Objekt um
    json_list = [json.loads(item.strip('"').replace('\\"', '"')) for item in data_list]

    return json_list


def convert_to_yolo_format(csv_file, output_folder, image_folder, animal, class_id):
    """Funktion liest die Label"""
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_names = set(os.listdir(image_folder))

    df = pd.read_csv(csv_file)
    df_animal = df.loc[df["common_name"].isin(animal)]
    wo_duplicates = df_animal.drop_duplicates(subset="location")
    print(wo_duplicates.shape)
    for index, row in tqdm(wo_duplicates.iterrows()):
        muster = r"[^/]+$"
        dateiname = re.search(muster, row["location"]).group()
        bb_str = wo_duplicates["bounding_boxes"][index]
        try:
            if (
                bb_str == ""
                or bb_str is None
                or bb_str is np.nan
                or dateiname not in image_names
            ):
                continue
            bounding_boxes = convert_to_json(bb_str)
            # print(bounding_boxes)
            yolo_data = []
            for box in bounding_boxes:
                if isinstance(box, str):
                    box = json.loads(box)  # Parse the string to a dictionary
                detection_box = box["detectionBox"]
                yolo_format = convert_box_to_yolo(detection_box, class_id)
                yolo_data.append(yolo_format)

            # Write YOLO data to a text file named after the image_id
            output_file = os.path.join(output_folder, f"{dateiname[:-4]}.txt")
            with open(output_file, mode="w") as out_file:
                for item in yolo_data:
                    out_file.write(" ".join(map(str, item)) + "\n")
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError for image_id {dateiname}: {e}")
            exit()
        except Exception as e:
            print(f"JSONDecodeError for image_id {dateiname}: {e}")
            print(type(bb_str))
            print(bb_str)
            exit()
            continue


def convert_box_to_yolo(detection_box, class_id):
    # YOLO format: [class, x_center, y_center, width, height]
    # Assuming class is 0 for all boxes
    x_center = (detection_box[1] + detection_box[3]) / 2
    y_center = (detection_box[0] + detection_box[2]) / 2
    width = detection_box[3] - detection_box[1]
    height = detection_box[2] - detection_box[0]
    return [class_id, x_center, y_center, width, height]


def move_files(src_dir, dest_dir, file_extension, percentage):

    os.makedirs(dest_dir, exist_ok=True)

    # Liste der Dateien mit der angegebenen Erweiterung erhalten
    files = [f for f in os.listdir(src_dir) if f.endswith(file_extension)]

    # Anzahl der zu verschiebenden Dateien berechnen
    num_files_to_move = int(len(files) * percentage)

    # Dateien zufällig auswählen
    files_to_move = random.sample(files, num_files_to_move)

    # Dateien verschieben und ihre Namen speichern
    moved_files = []
    for file in files_to_move:
        shutil.move(os.path.join(src_dir, file), os.path.join(dest_dir, file))
        moved_files.append(file)

    return moved_files


def move_text_files(src_dir, dest_dir, file_names):
    os.makedirs(dest_dir, exist_ok=True)

    for file_name in file_names:
        text_file = os.path.splitext(file_name)[0] + ".txt"
        if os.path.exists(os.path.join(src_dir, text_file)):
            shutil.move(
                os.path.join(src_dir, text_file), os.path.join(dest_dir, text_file)
            )


def shuffle_files(directory):
    files = os.listdir(directory)
    random.shuffle(files)
    for i, file in enumerate(files):
        src = os.path.join(directory, file)
        dst = os.path.join(directory, f"{i}_{file}")
        os.rename(src, dst)


def rename_files_in_directory(directory):
    """
    Löscht 'Zahl_' vor jedem File eines Ordners.
    Grund: Funktion shuffle_files erzeugt dieses Format.
    """
    # Liste der Dateien im Verzeichnis erhalten
    files = os.listdir(directory)

    for file in files:
        # Neuen Dateinamen erstellen, indem alles vor dem Unterstrich entfernt wird
        new_name = re.sub(r"^[^_]*_", "", file)

        # Alte und neue Dateipfade erstellen
        old_file_path = os.path.join(directory, file)
        new_file_path = os.path.join(directory, new_name)

        # Datei umbenennen
        os.rename(old_file_path, new_file_path)


"""Label umformatieren."""
# # Pfade
# image_folder = ".data/not_used/wi_wild_boar/images_w_label"
# csv_file = ".contrib/images_2004096.csv"
# output_folder = ".data/not_used/wi_wild_boar/labels"
# animal = ("Wild Boar",)  # Name des Tiers in der Spalte "common_name"
# class_id = 1  # id in data.yml für Klasse
# convert_to_yolo_format(csv_file, output_folder, image_folder, animal, class_id)

# print(
#     f"Die Bounding Boxen wurden erfolgreich in das YOLO-Format konvertiert und im Ordner {output_folder} gespeichert."
# )

"""Files verschieben und neu anordnen."""
# Verzeichnisse für Bilder
# Ordnernamen = ["validation", "test", "train"]
# for Ordnername in Ordnernamen:
#     src_image_dir = ".data/not_used/wi_wild_boar/images_w_label"
#     src_text_dir = ".data/not_used/wi_wild_boar/labels"

#     if Ordnername == "validation":
#         dest_image_dir = ".data/data_deer_wild_boar_yolo/validation/images"
#         dest_text_dir = ".data/data_deer_wild_boar_yolo/validation/labels"
#         size_of_data_part = 0.05
#     elif Ordnername == "test":
#         dest_image_dir = ".data/data_deer_wild_boar_yolo/test/images"
#         dest_text_dir = ".data/data_deer_wild_boar_yolo/test/labels"
#         size_of_data_part = 0.15
#     elif Ordnername == "train":
#         dest_image_dir = ".data/data_deer_wild_boar_yolo/train/images"
#         dest_text_dir = ".data/data_deer_wild_boar_yolo/train/labels"
#         size_of_data_part = 1
#     else:
#         print("Falsche Eingabe des ORDNERNAMENS.")

#     # Bilder in train, test und validation unterteilen
#     moved_images = move_files(src_image_dir, dest_image_dir, ".JPG", size_of_data_part)

#     # Entsprechende Textdateien verschieben
#     move_text_files(src_text_dir, dest_text_dir, moved_images)

#     # Dateien in beiden Zielverzeichnissen zufällig neu anordnen
#     shuffle_files(dest_image_dir)
#     shuffle_files(dest_text_dir)

#     if Ordnername == "train":
#         rename_files_in_directory(".data/data_deer_wild_boar_yolo/validation/images")
# rename_files_in_directory(".data/data_deer_wild_boar_yolo/validation/labels")
# rename_files_in_directory(".data/data_deer_wild_boar_yolo/test/images")
# rename_files_in_directory(".data/data_deer_wild_boar_yolo/test/labels")
# rename_files_in_directory(".data/data_deer_wild_boar_yolo/train/images")
# rename_files_in_directory(".data/data_deer_wild_boar_yolo/train/labels")


#     print(f"{Ordnername} wurde erfolgreich verschoben und neu angeordnet.")

# print("Dateien wurden erfolgreich verschoben und neu angeordnet.")
