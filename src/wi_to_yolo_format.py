import csv
import json
import os
import random
import shutil
import re


def convert_to_json(data_str):
    # Überprüfen, ob der String leer ist
    if not data_str:
        return []

    # Entferne die äußeren geschweiften Klammern und teile den String in einzelne Detection-Boxen auf
    data_list = data_str.strip("{}").split('","')

    # Entferne die Anführungszeichen und wandle jede Detection-Box in ein JSON-Objekt um
    json_list = [json.loads(item.strip('"').replace('\\"', '"')) for item in data_list]

    return json_list


def convert_to_yolo_format(csv_file, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_names = set(os.listdir(".data/wi_wild_boar/images_w_label"))

    with open(csv_file, mode="r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            image_id = row["image_id"]
            bb_str = row["bounding_boxes"]
            try:
                if bb_str == "" or image_id + ".JPG" not in image_names:
                    continue
                bounding_boxes = convert_to_json(bb_str)
                # print(bounding_boxes)
                yolo_data = []
                for box in bounding_boxes:
                    if isinstance(box, str):
                        box = json.loads(box)  # Parse the string to a dictionary
                    detection_box = box["detectionBox"]
                    yolo_format = convert_box_to_yolo(detection_box)
                    yolo_data.append(yolo_format)

                # Write YOLO data to a text file named after the image_id
                output_file = os.path.join(output_folder, f"{image_id}.txt")
                with open(output_file, mode="w") as out_file:
                    for item in yolo_data:
                        out_file.write(" ".join(map(str, item)) + "\n")
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError for image_id {image_id}: {e}")
                exit()
                continue


def convert_box_to_yolo(detection_box):
    # YOLO format: [class, x_center, y_center, width, height]
    # Assuming class is 0 for all boxes
    class_id = 1
    x_center = (detection_box[1] + detection_box[3]) / 2
    y_center = (detection_box[0] + detection_box[2]) / 2
    width = detection_box[3] - detection_box[1]
    height = detection_box[2] - detection_box[0]
    return [class_id, x_center, y_center, width, height]


def move_files(src_dir, dest_dir, file_extension, percentage):
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


"""Filename nach verschieben korrigieren."""
# rename_files_in_directory(".data/data_deer_wild_boar_yolo/validation/images")

"""Files verschieben und neu anordnen."""
# # Verzeichnisse für Bilder
# src_image_dir = ".data/wi_wild_boar/images_w_label"
# dest_image_dir = ".data/data_deer_wild_boar_yolo/validation/images"

# # Verzeichnisse für Textdateien
# src_text_dir = ".data/wi_wild_boar/labels"
# dest_text_dir = ".data/data_deer_wild_boar_yolo/validation/labels"

# # 5% der Bilder verschieben und ihre Namen erhalten
# moved_images = move_files(src_image_dir, dest_image_dir, ".JPG", 0.05)

# # Entsprechende Textdateien verschieben
# move_text_files(src_text_dir, dest_text_dir, moved_images)

# # Dateien in beiden Zielverzeichnissen zufällig neu anordnen
# shuffle_files(dest_image_dir)
# shuffle_files(dest_text_dir)

# print("Dateien wurden erfolgreich verschoben und neu angeordnet.")


"""Label umformatieren."""
# # Beispielverwendung
# csv_file = ".data/wi_wild_boar/labels/images_2004096.csv"
# output_folder = ".data/wi_wild_boar/labels"

# convert_to_yolo_format(csv_file, output_folder)

# print(
#     f"Die Bounding Boxen wurden erfolgreich in das YOLO-Format konvertiert und im Ordner {output_folder} gespeichert."
# )
