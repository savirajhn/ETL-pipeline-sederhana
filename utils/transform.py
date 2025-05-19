import pandas as pd
import re

def process_data(data):
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)
    
    # Rename columns if needed (assuming the column might have a different name)
    if 'name' in df.columns:
        df = df.rename(columns={'name': 'product_name'})
    
    # Remove invalid product names and null values
    df = df[df['product_name'].notna()]
    df = df[~df['product_name'].isin(['Unknown Product', 'N/A', ''])]
    
    # Bersihkan kolom 'price' dan tangani nilai tidak valid
    def clean_price(x):
        if pd.isnull(x) or x == 'Price Unavailable':
            return 0
        try:
            return int(float(re.sub(r'[$,]', '', str(x))) * 16000)
        except:
            return 0
    
    df['price'] = df['price'].apply(clean_price)
    
    # Bersihkan kolom 'rating'
    def clean_rating(x):
        if pd.isnull(x):
            return 0
        match = re.search(r"([\d.]+)", str(x))
        return float(match.group(1)) if match else 0
    
    df['rating'] = df['rating'].apply(clean_rating)
    
    # Bersihkan kolom 'colors'
    def clean_colors(x):
        if pd.isnull(x):
            return 0
        match = re.search(r"(\d+)", str(x))
        return int(match.group(1)) if match else 0
    
    df['colors'] = df['colors'].apply(clean_colors)
    
    # Bersihkan 'size'
    df['size'] = df['size'].fillna('One Size')
    df['size'] = df['size'].apply(lambda x: x.replace("Size:", "").strip() if isinstance(x, str) and "Size:" in x else x)
    
    # Bersihkan 'gender'
    df['gender'] = df['gender'].fillna('Unisex')
    df['gender'] = df['gender'].apply(lambda x: x.replace("Gender:", "").strip() if isinstance(x, str) and "Gender:" in x else x)
    
    # Remove duplicates and reset index
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    
    return df
