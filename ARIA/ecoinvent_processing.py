# ecoinvent_processing.py

import pandas as pd
import re

def process_ecoinvent_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Output columns: [Input/output, In/out, Units, Process, Location]
    'Units', 'Process', 'Location' come from splitting 'Ecoinvent process' on '|'.
    The original 'Ecoinvent process' column is dropped.
    """
    if "Ecoinvent process" not in df.columns:
        raise KeyError("'Ecoinvent process' column not found in the DataFrame.")

    s = df["Ecoinvent process"].astype(str)

    # Remove a leading dash and surrounding spaces, but DO NOT 'clean' away pipes
    s = s.str.replace(r"^\s*-\s*", "", regex=True).str.strip()

    # Split on a LITERAL pipe into at most 3 fields
    parts = s.str.split(r"\|", n=2, expand=True)

    # If some rows don't have all three parts, add missing columns
    while parts.shape[1] < 3:
        parts[parts.shape[1]] = ""

    # Strip whitespace
    parts[0] = parts[0].str.strip()
    parts[1] = parts[1].str.strip()
    parts[2] = parts[2].str.strip()

    # Build the final DataFrame (same structure you requested)
    out = pd.DataFrame({
        "Input/output": df["Input/output"],
        "In/out": df["In/out"],
        "Units": parts[2],     # from the ecoinvent string
        "Process": parts[0],
        "Location": parts[1],
    })

    return out


