import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe

def save_to_csv(df, filename='products.csv'):
    df.to_csv(filename, index=False)

def save_to_google_sheets(df, json_keyfile='projectetl-460308-e98a6a1bcc21.json', sheet_url='https://docs.google.com/spreadsheets/d/18ODNknHVafCQTzKCMLgGJikjfDmJJD8NVgVYyqmU3Es'):
    gc = gspread.service_account(filename=json_keyfile)
    sh = gc.open_by_url(sheet_url)
    worksheet = sh.sheet1
    worksheet.clear()
    set_with_dataframe(worksheet, df)
