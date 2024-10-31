from ultralytics import YOLO

# Load a COCO-pretrained YOLOv8n model
model = YOLO("yolov8n.pt")

# Display model information (optional)
model.info()

# for name, param in model.model.named_parameters():
#     print(name)


# Train the model on the COCO8 example dataset for 100 epochs
results = model.train(
    data="data.yaml",
    epochs=10,
    imgsz=640,
    batch=20,
    optimizer="ADAM",
    cache=True,
    momentum=0.9,
    lr0=0.001,
)

# model.save("path_to_your_model.h5")

# from tensorflow.keras.models import load_model

# model = load_model("path_to_your_yolo_model.h5")


# # Modell anhand der Testdaten evaluieren
# metrics = model.val(data='data.yaml')

# # Modell auf neuen Bildern testen
# path_test = "C:/Users/Z0127829/Downloads/train-yolov8-custom-dataset-step-by-step-guide/model_training/data/test"
# results = model.predict(source=path_test, save=True)


# # Wende das Modell auf das Bild an
# results = model(img)
# results


# for result in results:
#     boxes = result.boxes.xyxy  # Bounding Boxes
#     labels = result.boxes.cls  # Klassenlabels
#     scores = result.boxes.conf  # Konfidenzwerte

#     # Zeichne die Bounding Boxes und Labels auf das Bild
#     for box, label, score in zip(boxes, labels, scores):
#         x1, y1, x2, y2 = map(int, box)
#         class_name = result.names[int(label)]
#         confidence = float(score)

#         # Zeichne das Rechteck
#         cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

#         # Füge das Label und die Konfidenz hinzu
#         text = f'{class_name} {confidence:.2f}'
#         cv2.putText(img, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# # Zeige das Bild mit Matplotlib an
# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# plt.axis('off')
# plt.show()
