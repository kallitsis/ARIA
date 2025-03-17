# test_impact_assessment.py
import pytest
import pandas as pd
from ARIA.impact_assessment import run_impact_assessment

@pytest.mark.usefixtures("mock_bw")
def test_run_impact_assessment():
    df = pd.DataFrame({
        "Process": ["dummy process"],
        "Location": ["GLO"],
        "In/out": [1.5]
    })
    lcia_methods = [
        ("EF v3.1", "climate change", "global warming potential (GWP100)")
    ]

    out_df = run_impact_assessment(df, lcia_methods, "ecoinvent-3.10.1-cutoff")

    # Because LCA score = 42, 'In/out' = 1.5 => expected GWP = 63
    assert len(out_df) == 1, "Row should remain if there's a match"
    assert out_df.loc[0, "GWP"] == 63, "Expected GWP to be 63 (1.5 * 42)."
