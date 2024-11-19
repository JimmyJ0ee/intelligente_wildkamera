import csv
import json
import os
import pandas as pd


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

    image_names = set(os.listdir("./../.data/wi_wild_boar/images_w_label"))

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
    class_id = 0
    x_center = (detection_box[1] + detection_box[3]) / 2
    y_center = (detection_box[0] + detection_box[2]) / 2
    width = detection_box[3] - detection_box[1]
    height = detection_box[2] - detection_box[0]
    return [class_id, x_center, y_center, width, height]


# Beispielverwendung
csv_file = "./../.data/wi_wild_boar/labels/images_2004096.csv"
output_folder = "./../.data/wi_wild_boar/labels"

convert_to_yolo_format(csv_file, output_folder)

print(
    f"Die Bounding Boxen wurden erfolgreich in das YOLO-Format konvertiert und im Ordner {output_folder} gespeichert."
)
