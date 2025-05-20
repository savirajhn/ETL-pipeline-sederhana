import pytest
import pandas as pd
from utils.utils import transform as transform_data

def test_transform_data():
    data = {
        'price': ['$100', '$200', '$150', '$50'],
        'rating': ['⭐ 4.5 / 5', '⭐ 3.8 / 5', '⭐ 4.2 / 5', '⭐ 5.0 / 5'],
        'colors': ['3 Colors', '2 Colors', '4 Colors', '5 Colors'],
        'size': ['Size: M', 'Size: L', 'Size: S', 'Size: XL'],
        'gender': ['Gender: Men', 'Gender: Women', 'Gender: Unisex', 'Gender: Women'],
        'title': ['Product 1', 'Product 2', 'Product 3', 'Product 4'],
        'timestamp': ['2025-05-19T14:46:30.289406'] * 4,
        'image_url': ['url'] * 4
    }
    df = pd.DataFrame(data)
    df_transformed = transform_data(df)

    assert not df_transformed.empty
    assert pd.api.types.is_numeric_dtype(df_transformed['price'])
    assert pd.api.types.is_numeric_dtype(df_transformed['rating'])
    assert pd.api.types.is_numeric_dtype(df_transformed['colors'])
    assert all(isinstance(s, str) for s in df_transformed['size'])
    assert all(isinstance(g, str) for g in df_transformed['gender'])
    assert 'image_url' not in df_transformed.columns

def test_transform_filter_invalid_price_and_rating():
    raw_data = [
        {
            "title": "Unknown Product",
            "price": "Price Unavailable",
            "rating": "Invalid Rating",
            "colors": "3 Colors",
            "size": "Size: M",
            "gender": "Gender: Men",
            "image_url": "http://x",
            "timestamp": "2025-05-19T14:46:30.289406"
        },
        {
            "title": "Pants",
            "price": "$0.00",
            "rating": "⭐ 0 / 5",
            "colors": "0 Colors",
            "size": "Size: L",
            "gender": "Gender: Women",
            "image_url": "http://x",
            "timestamp": "2025-05-19T14:46:30.289406"
        }
    ]
    df = transform_data(raw_data)
   
    assert df.empty
