from utils.utils_extract import fetch_products
from utils.utils_transform import process_data
from utils.utils_load import save_to_csv, save_to_google_sheets


def main():
    raw_data = fetch_products(pages=50)
    df = process_data(raw_data)
    save_to_csv(df)
    save_to_google_sheets(df, json_keyfile='projectetl-460308-5f9f750dec66.json')

if __name__ == "__main__":
    main()