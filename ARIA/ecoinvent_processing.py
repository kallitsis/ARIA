# ecoinvent_processing.py

import re
import pandas as pd

def process_ecoinvent_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes a DataFrame by cleaning and splitting the 'Ecoinvent process' column into 'Process' and 'Location',
    as well as extracting 'Units'.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the 'Ecoinvent process' column to be processed.
    
    Returns:
        pd.DataFrame: The processed DataFrame with 'Process', 'Location', and 'Units' columns.
    """
    # Ensure the 'Ecoinvent process' column exists
    if "Ecoinvent process" not in df.columns:
        raise KeyError("'Ecoinvent process' column not found in the DataFrame.")

    # Function to clean the text in the 'Ecoinvent process' column
    def clean_text(text: str) -> str:
        # Allow word characters, spaces, commas, slashes, and hyphens
        text = re.sub(r"[^\w\s,/%\-]", '', text)
        return text.strip()

    # Clean the 'Ecoinvent process' column
    df["Ecoinvent process"] = df["Ecoinvent process"].apply(clean_text)

    # Split the 'Ecoinvent process' column based on the last comma to isolate units
    df["Ecoinvent process"] = df["Ecoinvent process"].str.lstrip("- ").str.strip()
    df[["Process_location", "Units"]] = df["Ecoinvent process"].str.rsplit(",", n=1, expand=True)
    df["Process_location"] = df["Process_location"].str.strip()
    df["Units"] = df["Units"].str.strip()

    # Drop the original 'Ecoinvent process' column
    df.drop(columns=["Ecoinvent process"], inplace=True)

    # Split 'Process_location' based on the last comma to isolate location
    df["Process_location"] = df["Process_location"].str.lstrip("- ").str.strip()
    df[["Process", "Location"]] = df["Process_location"].str.rsplit(",", n=1, expand=True)
    df["Process"] = df["Process"].str.strip()
    df["Location"] = df["Location"].str.strip()

    # Drop the temporary 'Process_location' column
    df.drop(columns=["Process_location"], inplace=True)

    return df
