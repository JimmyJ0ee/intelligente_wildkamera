import requests
from bs4 import BeautifulSoup
import os
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Warnungen unterdrücken
urllib3.disable_warnings(InsecureRequestWarning)


def test_img(response_content, img_url):
    from PIL import Image
    import io

    try:
        img = Image.open(io.BytesIO(response_content))
        img.show()  # Zeigt das Bild an
        img.save(
            os.path.join("images", os.path.basename(img_url))
        )  # Speichert das Bild
        print("Bild erfolgreich heruntergeladen und angezeigt.")
        return True
    except (IOError, SyntaxError) as e:
        print(f"Fehler beim Öffnen des Bildes: {e}")
    return False


def download_img_from_emammal():
    url = "https://emammal.si.edu/animal-photos?field_common_name_value=wild%20boar&field_scientific_name_value=&title=&page=5"
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
        if "eMammal_logo_black_1" in img_url:
            continue
        # Vollständige URL erstellen, falls nötig
        if not img_url.startswith("http"):
            img_url = home_url + img_url
            print(img_url)
        response = requests.get(img_url, verify=False)

        if test_img(response.content, img_url):
            img_data = requests.get(img_url, verify=False).content
            img_name = os.path.join("images", os.path.basename(img_url))
            with open(img_name, "wb") as handler:
                handler.write(img_data)
    print("Bilder wurden erfolgreich heruntergeladen und gespeichert.")

    return response


def download_img_from_wildlife_insights():
    # Erstelle eine Session
    # session = requests.Session()

    # Füge die Cookies hinzu (ersetze 'deine_cookies' durch die tatsächlichen Cookies)
    # cookies = {
    #     "_hjSessionUser_1248251": "eyJpZCI6IjI3MmYxYTYwLTE3YWQtNWFiYi05Yjk5LTBlYmIxYTZkMmM5MyIsImNyZWF0ZWQiOjE3Mjc5NTg2ODY4OTcsImV4aXN0aW5nIjp0cnVlfQ",
    #     "_ga": "GA1.2.1831113191.1727873567",
    #     "connect.sid": "s%3A501uIjtpSrtWLWJH0r_AIa0Kf4QXv35e.KGnOB%2BdW9kpjzm77Qk6jOlCvOsK3gpO4As8E6LhuksQ",
    # }
    # session.cookies.update(cookies)
    # print(session)
    url = "https://app.wildlifeinsights.org/download/2006898/project/2004865/data-files/d5fd84d9-17a8-4f1c-b80d-7dd261468fd7"
    # HTTP-Anfrage an die Webseite
    # response = session.get(url, verify=False)

    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    # Verzeichnis zum Speichern der Bilder
    os.makedirs("images", exist_ok=True)

    # Alle Bild-Tags finden
    img_tags = soup.find_all("img", recursive=True)
    print(img_tags)
    # Bilder herunterladen und speichern
    with open("page.html", "w", encoding="utf-8") as file:
        file.write(response.text)

    for img in img_tags:
        img_url = img["src"]
        # Vollständige URL erstellen, falls nötig
        if not img_url.startswith("http") or img_url.startswith("https"):
            img_url = url + img_url
        print(img_url)
        response = requests.get(img_url, verify=False)
        print(response.content)

        if test_img(response.content, img_url):
            img_data = requests.get(img_url, verify=False).content
            img_name = os.path.join("images", os.path.basename(img_url))
            with open(img_name, "wb") as handler:
                handler.write(img_data)

    print("Bilder wurden erfolgreich heruntergeladen und gespeichert.")

    return response


def download_img_from_iNaturalist():
    url = "https://www.inaturalist.org/observations?reviewed=true&subview=table&taxon_id=421345"
    home_url = "https://www.inaturalist.org/"
    # HTTP-Anfrage an die Webseite
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    with open("page.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    # Verzeichnis zum Speichern der Bilder
    os.makedirs("images", exist_ok=True)

    # Alle Bild-Tags finden
    a_tags = soup.find_all("a", class_="img", recursive=True)
    print(a_tags)
    print(f"Anzahl der gefundenen <a>-Tags: {len(a_tags)}")

    # Bilder herunterladen und speichern
    for a_tag in a_tags:
        img_url = a_tag.get("href")
        # Vollständige URL erstellen, falls nötig
        if not img_url.startswith("http"):
            img_url = home_url + img_url
            print(img_url)
        response = requests.get(img_url, verify=False)

        if test_img(response.content, img_url):
            img_data = requests.get(img_url, verify=False).content
            img_name = os.path.join("images", os.path.basename(img_url))
            with open(img_name, "wb") as handler:
                handler.write(img_data)
    print("Bilder wurden erfolgreich heruntergeladen und gespeichert.")

    return response


# download_img_from_wildlife_insights()
download_img_from_iNaturalist()
