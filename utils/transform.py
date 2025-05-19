import re
import pandas as pd
import numpy as np

EXCHANGE_RATE = 16000

def transform(data: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(data)
    # Hapus baris dengan 'Price Unavailable'
    df = df[~df["price"].str.contains("Unavailable", na=False)]
    # Bersihkan harga: hapus simbol dan ubah ke IDR
    df["price"] = df["price"].str.replace("[$,]", "", regex=True).astype(float) * EXCHANGE_RATE

    # Rating: ambil angka dari teks dan ubah koma ke titik
    df["rating"] = df["rating"].str.replace(",", ".").str.extract(r"([\d.]+)").astype(float)

    # Colors: ambil angka jumlah warna
    df["colors"] = df["colors"].str.extract(r"(\d+)").astype(float).astype("Int64")

    # Size & Gender: hapus prefix
    df["size"] = df["size"].str.replace("Size:", "").str.strip()
    df["gender"] = df["gender"].str.replace("Gender:", "").str.strip()

    # Drop baris tidak lengkap
    df = df.dropna(subset=["title", "price", "rating", "colors", "size", "gender", "timestamp"])

    # Hapus produk 'Unknown Product' dan 'Pants'
    df = df[~df["title"].isin(["Unknown Product", "Pants"])]

    # Ganti nilai 0 menjadi NaN lalu drop
    for col in ["price", "rating", "colors"]:
        df[col] = df[col].replace(0, np.nan)
    df = df.dropna(subset=["price", "rating", "colors"])

    # Validasi rating: antara 1 dan 5
    df = df[df["rating"].between(1.0, 5.0)]

    # Hapus duplikat
    df = df.drop_duplicates()

    return df
