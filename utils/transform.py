import re
import pandas as pd
import numpy as np

EXCHANGE_RATE = 16000

def transform(data: list[dict]) -> pd.DataFrame:
    try:
        df = pd.DataFrame(data)
    except Exception as e:
        print(f"[ERROR] Gagal membuat DataFrame: {e}")
        return pd.DataFrame()

    try:
        df = df[~df["price"].str.contains("Unavailable", na=False)]
        df["price"] = df["price"].str.replace("[$,]", "", regex=True).astype(float) * EXCHANGE_RATE
        df["rating"] = df["rating"].str.replace(",", ".").str.extract(r"([\d.]+)").astype(float)
        df["colors"] = df["colors"].str.extract(r"(\d+)").astype(float).astype("Int64")
        df["size"] = df["size"].str.replace("Size:", "").str.strip()
        df["gender"] = df["gender"].str.replace("Gender:", "").str.strip()
        df = df.dropna(subset=["title", "price", "rating", "colors", "size", "gender", "timestamp"])
        df = df[~df["title"].isin(["Unknown Product", "Pants"])]
        for col in ["price", "rating", "colors"]:
            df[col] = df[col].replace(0, np.nan)
        df = df.dropna(subset=["price", "rating", "colors"])
        df = df[df["rating"].between(1.0, 5.0)]
        df = df.drop_duplicates()
        if "image_url" in df.columns:
            df = df.drop(columns=["image_url"])
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat transformasi data: {e}")
        return pd.DataFrame()

    return df
