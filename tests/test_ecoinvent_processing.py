# test_ecoinvent_processing.py

import pytest
import pandas as pd
from ARIA.ecoinvent_processing import process_ecoinvent_dataframe

def test_process_ecoinvent_dataframe():
    data = {
        "Ecoinvent process": [
            "- some process, GLO, kg",
            "my process location, RER, p"
        ]
    }
    df = pd.DataFrame(data)
    processed = process_ecoinvent_dataframe(df)
    
    assert "Process" in processed.columns
    assert "Location" in processed.columns
    assert "Units" in processed.columns
    
    assert processed.loc[0, "Process"] == "some process"
    assert processed.loc[0, "Location"] == "GLO"
    assert processed.loc[0, "Units"] == "kg"
