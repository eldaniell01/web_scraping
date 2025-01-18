import requests
from bs4 import BeautifulSoup
import re


url = "https://www.amazon.com/dp/B07B3YXSTG#customerReviews"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
title1 = soup.find("span", {"id": "productTitle"}).get_text(strip=True)
title_clean = re.sub(r'[\\/*?:"<>|]', "_", title1)
with open(f"{title_clean}.txt", "w") as file:
    if response.status_code == 200:
        # Parsear el contenido de la página
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscar la tabla de desglose de calificaciones
        title = soup.find("span", {"id": "productTitle"}).get_text(strip=True)
        rating_table = soup.find("ul", {"id": "histogramTable"})
        total_count = soup.find("div", {"class": "a-row a-spacing-medium averageStarRatingNumerical"})
        details_table = soup.find("table", {"id": "productDetails_detailBullets_sections1"})
        
        print(title)
        file.write(f"{title}\n")
        if total_count:
            votes = total_count.find("span", {"class": "a-size-base a-color-secondary"}).get_text(strip=True)
            print(votes)
            file.write(f"{votes}\n")
        
        if details_table:
            elements = details_table.find_all("tr")
            for row in elements:
            # Buscar el <th> y <td> específicos dentro de la fila
                item1 = row.find("th", {"class": "a-color-secondary a-size-base prodDetSectionEntry"})
                item2 = row.find("td", {"class": "a-size-base prodDetAttrValue"})
                
                # Verificar si ambos elementos fueron encontrados
                if item1 and item2:
                    item1_text = item1.get_text(strip=True)
                    item2_text = item2.get_text(strip=True)
                    print(f"{item1_text}:------------{item2_text}")
                    file.write(f"{item1_text}:------------{item2_text}\n")
            
        if rating_table:
            print("Desglose de reseñas por calificación:")
            file.write(f"Desglose de reseñas por calificación:\n")
            items = rating_table.find_all("li")
            for item in items:
                try:
                    # Encontrar el div con la información de estrellas
                    stars_div = item.find("div", {"class": "a-section a-spacing-none a-text-left aok-nowrap"})
                    if stars_div:
                        # Obtener solo el texto directo del div, ignorando los spans
                        stars = ''.join(stars_div.find_all(string=True, recursive=False)).strip()

                    # Extraer el conteo directamente
                    count_div = item.find("div", {"class": "a-section a-spacing-none a-text-right aok-nowrap"})
                    if count_div:
                        # Obtener solo el texto fuera de los spans
                        count = ''.join(count_div.find_all(string=True, recursive=False)).strip()
                        
                    print(f"{stars}: {count}")
                    file.write(f"{stars}: {count}\n")
                except AttributeError:
                    continue
    else:
        print(f"Error al acceder a la página: {response.status_code}")