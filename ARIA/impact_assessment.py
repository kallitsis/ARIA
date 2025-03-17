import brightway2 as bw
import pandas as pd

def run_impact_assessment(
    processed_df: pd.DataFrame,
    lcia_methods: list,
    ecoinvent_db_name: str = "ecoinvent-3.10.1-cutoff"
) -> pd.DataFrame:
    """
    Runs an LCIA impact assessment on each row of the given DataFrame,
    using the specified ecoinvent database and list of LCIA methods.

    Parameters
    ----------
    processed_df : pd.DataFrame
        A DataFrame that must contain 'Process', 'Location', and 'In/out' columns.
    lcia_methods : list
        A list of LCIA method tuples of the form (method_package, method_name, method_indicator).
    ecoinvent_db_name : str, optional
        The name of the ecoinvent database to use, by default 'ecoinvent-3.10.1-cutoff'.

    Returns
    -------
    pd.DataFrame
        The same DataFrame, updated with impact category columns (e.g., 'GWP', 'ADP', 'Water use', etc.).
    """
    # 1) Ensure the Ecoinvent database is loaded
    if ecoinvent_db_name not in bw.databases:
        print(f"Ecoinvent database '{ecoinvent_db_name}' not found. Please ensure it is loaded.")
        return processed_df  # Return unmodified DataFrame

    # 2) Ensure 'In/out' is numeric and fill missing values (avoid inplace to prevent chained assignment warnings)
    processed_df["In/out"] = pd.to_numeric(processed_df["In/out"], errors="coerce")
    processed_df["In/out"] = processed_df["In/out"].fillna(0)

    # 3) Create columns for each impact category you might track.
    impact_cols = {
        "GWP": None,
        "ADP": None,
        "Water use": None,
        "AP": None,
        "FETP": None,
        "HTP": None,   # Carcinogenic human toxicity potential
        "ODP": None,
        "PMFP": None,
        "POFP": None,
    }
    for col in impact_cols:
        processed_df[col] = None

    # 4) Loop over each row and perform LCIA for the matched process
    sp = bw.Database(ecoinvent_db_name)  # The ecoinvent database object
    for idx, row in processed_df.iterrows():
        # Strip whitespace just in case
        process_name = str(row["Process"]).strip()
        location = str(row["Location"]).strip()

        print(f"Checking process: {process_name} in {location}")

        # Find potential matches in the database
        results = [
            act for act in sp
            if act["name"] == process_name and act["location"] == location
        ]
        print(f"Number of matches found: {len(results)}")

        if results:
            selected_result = results[0]  # Example: select the first match
            print(f"Selected match for '{process_name}' in '{location}': {selected_result}")

            # Build the functional unit
            functional_unit = {selected_result: 1}

            # Calculate impact for each LCIA method
            for method in lcia_methods:
                lca = bw.LCA(functional_unit, method)
                lca.lci()
                lca.lcia()

                if not isinstance(lca.score, (int, float)) or pd.isna(lca.score):
                    print(f"Warning: LCA score for {method} is invalid (NaN or non-numeric).")
                    continue

                # Adjust by the 'In/out' quantity
                adjusted_impact = row["In/out"] * lca.score

                if "global warming potential (GWP100)" in method[2]:
                    processed_df.at[idx, "GWP"] = adjusted_impact
                elif "abiotic depletion potential (ADP)" in method[2]:
                    processed_df.at[idx, "ADP"] = adjusted_impact
                elif "user deprivation potential" in method[2]:
                    processed_df.at[idx, "Water use"] = adjusted_impact
                elif "accumulated exceedance (AE)" in method[2]:
                    processed_df.at[idx, "AP"] = adjusted_impact
                elif "comparative toxic unit for ecosystems (CTUe)" in method[2]:
                    processed_df.at[idx, "FETP"] = adjusted_impact
                elif "comparative toxic unit for human (CTUh)" in method[2]:
                    processed_df.at[idx, "HTP"] = adjusted_impact
                elif "ozone depletion potential (ODP)" in method[2]:
                    processed_df.at[idx, "ODP"] = adjusted_impact
                elif ("impact on human health" in method[2]) and ("particulate matter" in method[1]):
                    processed_df.at[idx, "PMFP"] = adjusted_impact
                elif "tropospheric ozone concentration increase" in method[2]:
                    processed_df.at[idx, "POFP"] = adjusted_impact
        else:
            print(f"No matches found for '{process_name}' in '{location}'")

    # 5) Optionally remove rows where all impact columns are NaN
    #    If your test expects the row to remain, comment this out or adapt it.
    impact_columns = ["GWP", "ADP", "Water use", "AP", "FETP", "HTP", "ODP", "PMFP", "POFP"]
    processed_df.dropna(subset=impact_columns, how="all", inplace=True)

    return processed_df
