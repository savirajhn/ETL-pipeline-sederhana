import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe

def save_to_csv(df, filename='products.csv'):
    df.to_csv(filename, index=False)

def save_to_google_sheets(df, json_keyfile='projectetl-460308-900545cba476.json', sheet_url='https://docs.google.com/spreadsheets/d/1y4MjFD-gdprvLkIb7cEeH13x2aZAiWMiBzYVH5m2Md0/edit?gid=0#gid=0'):
    gc = gspread.service_account(filename=json_keyfile)
    sh = gc.open_by_url(sheet_url)
    worksheet = sh.sheet1
    worksheet.clear()
    set_with_dataframe(worksheet, df)
