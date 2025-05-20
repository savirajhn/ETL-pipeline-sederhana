import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils import load as load

def test_save_csv(tmp_path):
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    filename = tmp_path / "test_output.csv"  # pakai direktori sementara
    load.save_to_csv(df, filename)
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
    mock_sheet.sheet1 = mock_worksheet

    df = pd.DataFrame({'a': [1], 'b': [2]})
    load.save_to_google_sheets(df, 'dummy.json', 'https://dummyurl')
    mock_gc.open_by_url.assert_called_once_with('https://dummyurl')
    mock_worksheet.clear.assert_called_once()
