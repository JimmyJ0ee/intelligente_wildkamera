import requests
from bs4 import BeautifulSoup
import os


# URL der Webseite
# img_url = "https://app.wildlifeinsights.org/download/2006898/project/2004865/data-files/d5fd84d9-17a8-4f1c-b80d-7dd261468fd7"
url = "https://emammal.si.edu/node/119992"
home_url = "https://emammal.si.edu/"
# HTTP-Anfrage an die Webseite
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.text, "html.parser")
# Verzeichnis zum Speichern der Bilder
os.makedirs("images", exist_ok=True)

# Alle Bild-Tags finden
img_tags = soup.find_all("img", recursive=True)
print(img_tags)
# Bilder herunterladen und speichern

for img in img_tags:
    img_url = img["src"]
    # Vollständige URL erstellen, falls nötig
    if not img_url.startswith("http"):
        img_url = home_url + img_url
        print(img_url)
    response = requests.get(img_url, verify=False)
    print(response.content)

    img_data = requests.get(img_url, verify=False).content
    img_name = os.path.join("images", os.path.basename(img_url))
    with open(img_name, "wb") as handler:
        handler.write(img_data)

print("Bilder wurden erfolgreich heruntergeladen und gespeichert.")


from PIL import Image
import io

try:
    img = Image.open(io.BytesIO(response.content))
    img.show()  # Zeigt das Bild an
    img.save(os.path.join("images", os.path.basename(img_url)))  # Speichert das Bild
    print("Bild erfolgreich heruntergeladen und angezeigt.")
except (IOError, SyntaxError) as e:
    print(f"Fehler beim Öffnen des Bildes: {e}")
