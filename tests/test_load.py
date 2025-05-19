import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import save_csv, save_to_google_sheets

def test_save_csv():
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    filename = 'test_output.csv'
    save_csv(df, filename)
    # Cek file dibuat dan isinya
    df_loaded = pd.read_csv(filename)
    assert list(df_loaded.columns) == ['a', 'b']
    assert len(df_loaded) == 2

@patch('gspread.service_account')
def test_save_to_google_sheets(mock_service_account):
    mock_gc = MagicMock()
    mock_sheet = MagicMock()
    mock_worksheet = MagicMock()
    mock_service_account.return_value = mock_gc
    mock_gc.open_by_url.return_value = mock_sheet
    mock_sheet.get_worksheet.return_value = mock_worksheet

    df = pd.DataFrame({'a': [1], 'b': [2]})
    save_to_google_sheets(df, 'dummy.json', 'https://dummyurl')
    mock_gc.open_by_url.assert_called_once()
    mock_sheet.get_worksheet.assert_called_once()
    mock_worksheet.clear.assert_called_once()
