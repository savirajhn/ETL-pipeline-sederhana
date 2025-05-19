import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_products(pages=50):
    base_url = "https://fashion-studio.dicoding.dev"
    all_products = []

    for page in range(1, pages + 1):
        url = base_url if page == 1 else f"{base_url}/page{page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for card in soup.select("div.collection-card"):
            try:
                title = card.select_one("h3.product-title").get_text(strip=True)
                price = card.select_one(".price").get_text(strip=True)
                rating = card.select_one("div.product-details p").get_text(strip=True)
                colors = card.select("div.product-details p")[1].get_text(strip=True)
                size = card.select("div.product-details p")[2].get_text(strip=True)
                gender = card.select("div.product-details p")[3].get_text(strip=True)
                image_url = card.select_one("img.collection-image")['src']
                all_products.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "colors": colors,
                    "size": size,
                    "gender": gender,
                    "image_url": image_url,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except:
                continue
    return all_products
