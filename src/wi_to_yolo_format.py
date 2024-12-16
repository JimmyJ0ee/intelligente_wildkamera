import json
import os
import random
import shutil
import re
import pandas as pd
from tqdm import tqdm
import numpy as np
import time


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

    # Label lesen + Duplikate löschen
    df = pd.read_csv(csv_file)
    df_animal = df.loc[df["common_name"].isin(animal)]
    print(df.shape)
    # Doppelte Vorkommen sind evtl. 1x falsch klassifiziert. Löschen sichert Qualität des Datensatzes.
    wo_duplicates = df_animal["location"].drop_duplicates(keep=False)
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
                print(f"{e}\n{dateiname}")
            zaehler += 1
        else:
            source_file = os.path.join(image_folder, dateiname)
            destination_file = os.path.join(destination_folder_wo_label, dateiname)
            try:
                shutil.copy(source_file, destination_file)
            except FileNotFoundError as e:
                print(e, dateiname)
                print("Bild nicht vorhanden.")
    print(
        f"Anzahl der Bilder in der CSV: {zaehler} (Bilder ohne label, Label ohne Bilder und Duplikate gelöscht.)"
    )


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
    duplicates = []
    for file in files_to_move:
        if not os.path.exists(os.path.join(dest_dir, file)):
            shutil.move(os.path.join(src_dir, file), os.path.join(dest_dir, file))
            moved_files.append(file)
        else:
            os.remove(os.path.join(dest_dir, file))
            duplicates.append(file)
    print(f"\nBilder-Duplikate: {duplicates}")
    print(f"Anzahl der Duplikate: {len(duplicates)}")
    return moved_files


def move_text_files(src_dir, dest_dir, file_names):
    os.makedirs(dest_dir, exist_ok=True)
    duplicates = []
    duplicates_output = []

    for file_name in file_names:
        text_file = os.path.splitext(file_name)[0] + ".txt"
        if os.path.exists(os.path.join(src_dir, text_file)):
            if not os.path.exists(os.path.join(dest_dir, text_file)):
                shutil.move(
                    os.path.join(src_dir, text_file), os.path.join(dest_dir, text_file)
                )
    duplicates = [f for f in os.listdir(src_dir)]
    for element in duplicates:
        if os.path.exists(os.path.join(src_dir, element)) and os.path.exists(
            os.path.join(dest_dir, element)
        ):
            os.remove(os.path.join(dest_dir, element))
            duplicates_output.append(element)
    print(f"\nLabel-Duplikate: {duplicates_output}")
    print(f"Anzahl der Duplikate: {len(duplicates_output)}")


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
        try:
            os.rename(old_file_path, new_file_path)
        except PermissionError:
            print(f"PermissionError: {file} wird von einem anderen Prozess verwendet.")
            time.sleep(1)  # Warte eine Sekunde und versuche es erneut
            os.rename(old_file_path, new_file_path)


if __name__ == "__main__":
    """
    Anleitung:
    1. Parameter einstellen unter 'PARAMETER EINSTELLEN'.
    2. Pfade in Vorschleife rename() anpassen.
    3. GO!
    """

    """Bilder ohne Label und Duplikate löschen."""

    # PARAMETER EINSTELLEN
    image_folder = ".data/not_used/wi_badger/images"
    csv_file = ".contrib/images_2004096.csv"
    destination_folder_w_label = ".data/not_used/wi_badger/images_w_label"
    destination_folder_wo_label = ".data/not_used/wi_badger/images_wo_label"
    animal = (
        "Eurasian Badger",
    )  # Name des Tiers in der Spalte "common_name" ACHTUNG: Muss Tupel sein.

    split_images(
        image_folder,
        csv_file,
        destination_folder_w_label,
        destination_folder_wo_label,
        animal,
    )

    """Label umformatieren."""

    # PARAMETER EINSTELLEN
    image_folder = ".data/not_used/wi_badger/images_w_label"
    output_folder = ".data/not_used/wi_badger/labels"
    class_id = 3  # id in data.yml für Klasse

    convert_to_yolo_format(csv_file, output_folder, image_folder, animal, class_id)
    print(
        f"Die Bounding Boxen wurden erfolgreich in das YOLO-Format konvertiert und im Ordner {output_folder} gespeichert."
    )

    """Files verschieben und neu anordnen."""

    # PARAMETER EINSTELLEN
    Ordnernamen = ["validation", "test", "train"]
    for Ordnername in Ordnernamen:
        src_image_dir = ".data/not_used/wi_badger/images_w_label"
        src_text_dir = ".data/not_used/wi_badger/labels"

        if Ordnername == "validation":
            dest_image_dir = ".data/data_4animals/validation/images"
            dest_text_dir = ".data/data_4animals/validation/labels"
            size_of_data_part = 0.05
        elif Ordnername == "test":
            dest_image_dir = ".data/data_4animals/test/images"
            dest_text_dir = ".data/data_4animals/test/labels"
            size_of_data_part = 0.15
        elif Ordnername == "train":
            dest_image_dir = ".data/data_4animals/train/images"
            dest_text_dir = ".data/data_4animals/train/labels"
            size_of_data_part = 1
        else:
            print("Falsche Eingabe des ORDNERNAMENS.")

        # Bilder in train, test und validation unterteilen
        moved_images = move_files(
            src_image_dir, dest_image_dir, ".JPG", size_of_data_part
        )

        # Entsprechende Textdateien verschieben
        move_text_files(src_text_dir, dest_text_dir, moved_images)

        # Dateien in beiden Zielverzeichnissen zufällig neu anordnen
        shuffle_files(dest_image_dir)
        shuffle_files(dest_text_dir)

        if Ordnername == "train":
            rename_files_in_directory(".data/data_4animals/validation/images")
            rename_files_in_directory(".data/data_4animals/validation/labels")
            rename_files_in_directory(".data/data_4animals/test/images")
            rename_files_in_directory(".data/data_4animals/test/labels")
            rename_files_in_directory(".data/data_4animals/train/images")
            rename_files_in_directory(".data/data_4animals/train/labels")

        print(
            f"{Ordnername} wurde erfolgreich verschoben, zufällig angeordnet und die Benennung korrigiert."
        )

    print(
        f"\nAlle Dateien wurde erfolgreich verschoben, zufällig angeordnet und die Benennung korrigiert."
    )
