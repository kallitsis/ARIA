# test_data_handling.py

import pytest
import pandas as pd
from ARIA.data_handling import open_excel_with_applescript, read_and_clean_excel

def test_read_and_clean_excel(tmp_path):
    # Create a dummy Excel file
    dummy_xlsx = tmp_path / "test_data.xlsx"
    df = pd.DataFrame({"A": [1, 2, None], "B": [None, "test", "data"]})
    df.to_excel(dummy_xlsx, index=False)

    # Attempt to read and clean
    cleaned_df = read_and_clean_excel(str(dummy_xlsx), usecols="A:B", nrows=3)
    
    # We expect the row with any None to be dropped => only 1 valid row remains
    assert len(cleaned_df) == 1
    assert list(cleaned_df.columns) == ["A", "B"]

@pytest.mark.skip(reason="Requires a real Excel environment with AppleScript on macOS")
def test_open_excel_with_applescript():
    # This test is just a placeholder, as it requires macOS + MS Excel environment
    # In CI or on non-macOS systems, you'd typically skip or mock out AppleScript calls.
    open_excel_with_applescript("/path/to/non_existent.xlsx")
