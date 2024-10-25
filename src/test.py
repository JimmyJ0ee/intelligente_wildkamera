# import boto3

# # S3-Client erstellen
# s3 = boto3.client("s3")

# # Datei von S3 herunterladen
# s3.download_file(
#     "open-images-dataset", "validation/4d90bf7713c05800.jpg", "local_image.jpg"
# )

from PIL import Image


def crop_border(image_path, border_size):
    # Öffne die Bilddatei
    img = Image.open(image_path)

    # Berechne die Zuschneidebox (links, oben, rechts, unten)
    width, height = img.size
    left = border_size
    upper = border_size
    right = width - border_size
    lower = height - border_size

    # Schneide das Bild zu
    cropped_img = img.crop((0, 0, width, lower))

    return cropped_img


# Beispielverwendung
image_path = (
    "Kamera Gipfelkirrung (11).png"  # Ersetze dies durch den Pfad zu deinem Bild
)
border_size = 60  # Größe des abzuschneidenden Randes

cropped_image = crop_border(image_path, border_size)
cropped_image.save("Kamera Gipfelkirrung (11)_cropped.png")

print(
    "Der Rand wurde erfolgreich entfernt und das zugeschnittene Bild wurde als 'cropped_image.jpg' gespeichert."
)
