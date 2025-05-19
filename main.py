from utils.extract import fetch_products
from utils.transform import transform
from utils.load import save_to_csv, save_to_google_sheets


def main():
    raw_data = fetch_products(pages=50)
    df = transform(raw_data)
    save_to_csv(df)
    save_to_google_sheets(df, json_keyfile='projectetl-460308-7f6b758c3790.json')

if __name__ == "__main__":
    main()
