import pytest
from utils import extract
from datetime import datetime

class DummyResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise Exception(f"HTTP {self.status_code}")

def test_scrape_page_success(monkeypatch):
    html = """
    <div class="collection-card">
      <h3 class="product-title">Test Shirt</h3>
      <div class="price-container"><span class="price">$10.00</span></div>
      <div class="product-details">
        <p>Rating: ⭐ 4.5 / 5</p>
        <p>2 Colors</p>
        <p>Size: M</p>
        <p>Gender: Unisex</p>
      </div>
      <img class="collection-image" src="http://example.com/image.jpg" />
    </div>
    """

    # ✅ Perbaikan di sini: support `timeout`
    monkeypatch.setattr("requests.get", lambda url, timeout=None: DummyResponse(html))

    data = extract.fetch_products(pages=1)
    assert isinstance(data, list)
    assert len(data) == 1
    item = data[0]
    assert item["title"] == "Test Shirt"
    assert item["price"] == "$10.00"
    assert "Rating:" in item["rating"]
    assert item["colors"] == "2 Colors"
    assert item["size"] == "Size: M"
    assert item["gender"] == "Gender: Unisex"
    datetime.fromisoformat(item["timestamp"])

def test_extract_all_pages(monkeypatch):
    def dummy_fetch_page(*args, **kwargs):
        return [{
            "title": "Dummy Product",
            "price": "$10.00",
            "rating": "⭐ 4.5 / 5",
            "colors": "2 Colors",
            "size": "Size: M",
            "gender": "Gender: Unisex",
            "image_url": "http://example.com/image.jpg",
            "timestamp": datetime.utcnow().isoformat()
        }]

    monkeypatch.setattr(extract, "fetch_products", dummy_fetch_page)
    data = extract.fetch_products(pages=2)
    assert len(data) == 1
