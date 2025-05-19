import pandas as pd
import re

def process_data(data):
    df = pd.DataFrame(data)
    
    # Bersihkan kolom 'price' dan tangani nilai tidak valid
    def clean_price(x):
        if pd.isnull(x) or x == 'Price Unavailable':
            return 0
        try:
            return int(float(re.sub(r'[$,]', '', x)) * 16000)
        except:
            return 0
    
    df['price'] = df['price'].apply(clean_price)
    
    # Bersihkan kolom 'rating'
    def clean_rating(x):
        if pd.isnull(x):
            return 0
        match = re.search(r"([\d.]+)", x)
        return float(match.group(1)) if match else 0
    
    df['rating'] = df['rating'].apply(clean_rating)
    
    # Bersihkan kolom 'colors'
    def clean_colors(x):
        if pd.isnull(x):
            return 0
        match = re.search(r"(\d+)", x)
        return int(match.group(1)) if match else 0
    
    df['colors'] = df['colors'].apply(clean_colors)
    
    # Bersihkan 'size'
    df['size'] = df['size'].apply(lambda x: x.replace("Size:", "").strip() if "Size:" in x else x)
    
    # Bersihkan 'gender'
    df['gender'] = df['gender'].apply(lambda x: x.replace("Gender:", "").strip() if "Gender:" in x else x)
    
    return df
