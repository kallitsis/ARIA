# data_handling.py

import subprocess
import pandas as pd

def open_excel_with_applescript(file_path: str):
    """
    Opens the specified Excel file in Microsoft Excel using AppleScript.
    
    Parameters
    ----------
    file_path : str
        The absolute path to the Excel file to be opened.
    """
    applescript = f'''
    tell application "Microsoft Excel"
        open POSIX file "{file_path}"
        activate
    end tell
    '''
    # Call AppleScript via subprocess
    subprocess.call(["osascript", "-e", applescript])


def read_and_clean_excel(file_path: str, usecols: str = "A:C", nrows: int = 12):
    """
    Reads an Excel file into a DataFrame, removes rows with any NaN values, and resets the index.

    Parameters
    ----------
    file_path : str
        The path to the Excel file.
    usecols : str, optional
        The columns to read (e.g., 'A:C' for columns A to C).
    nrows : int, optional
        Number of rows to read from the Excel file.

    Returns
    -------
    pd.DataFrame
        The cleaned DataFrame.
    """
    data_frame = pd.read_excel(file_path, usecols=usecols, nrows=nrows)
    data_frame.dropna(inplace=True)
    data_frame.reset_index(drop=True, inplace=True)
    return data_frame
