import pytest
import pandas as pd
from utils.transform import transform_data

def test_transform_data():
    data = {
        'price': ['$100', '$200', 'N/A', None],
        'rating': ['⭐ 4.5 / 5', '⭐ 3.8 / 5', 'N/A', None],
        'colors': ['Red Blue', 'Green', None, 'Yellow Black'],
        'size': ['Size: M', 'Size: L', 'Size: S', None],
        'gender': ['Gender: Men', 'Gender: Women', None, 'Gender: Unisex'],
        'title': ['Product 1', 'Product 2', 'Product 3', 'Product 4']
    }
    df = pd.DataFrame(data)
    df_transformed = transform_data(df)
    # Pastikan 'price' sudah jadi numeric
    assert pd.api.types.is_numeric_dtype(df_transformed['price'])
    # Pastikan 'rating' sudah float
    assert all(isinstance(r, float) or pd.isna(r) for r in df_transformed['rating'])
    # Pastikan 'colors' dihitung jumlah warnanya
    assert all(isinstance(c, int) for c in df_transformed['colors'])
    # Pastikan 'size' dan 'gender' bersih dari teks
    assert all(isinstance(s, str) for s in df_transformed['size'])
    assert all(isinstance(g, str) for g in df_transformed['gender'])