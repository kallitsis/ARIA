# test_data_handling.py

import pytest
import pandas as pd
from ARIA.data_handling import open_excel_with_applescript, read_and_clean_excel

def test_read_and_clean_excel(tmp_path):
    # Create a dummy Excel file with some partial and fully missing rows
    dummy_xlsx = tmp_path / "test_data.xlsx"
    df = pd.DataFrame({"A": [1, 2, None, None], "B": [None, "test", "data", None]})
    df.to_excel(dummy_xlsx, index=False)

    # Attempt to read and clean
    cleaned_df = read_and_clean_excel(str(dummy_xlsx), usecols="A:B", nrows=4)

    # Current function drops only rows where ALL values are NaN
    # So only the last row (None, None) is dropped
    assert len(cleaned_df) == 3  # Only the last row dropped
    assert list(cleaned_df.columns) == ["A", "B"]

    # Optional: Check specific remaining rows if you want stricter assertions
    expected = pd.DataFrame({"A": [1.0, 2.0, None], "B": [None, "test", "data"]})
    pd.testing.assert_frame_equal(cleaned_df.reset_index(drop=True), expected)

@pytest.mark.skip(reason="Requires a real Excel environment with AppleScript on macOS")
def test_open_excel_with_applescript():
    open_excel_with_applescript("/path/to/non_existent.xlsx")

