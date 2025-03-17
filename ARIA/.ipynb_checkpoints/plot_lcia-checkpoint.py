# plot_lcia.py

import seaborn as sns
import plotly.graph_objects as go
import matplotlib.colors as mcolors
import pandas as pd

def format_numeric(value: float) -> str:
    """
    Format numeric values based on their magnitude.
    """
    if abs(value) < 0.01:
        return f'{value:.2e}'  # Scientific notation with 2 sig digits
    else:
        return f'{value:.2f}'  # Fixed-point notation for larger values

def plot_lcia_waterfall_charts(processed_df: pd.DataFrame) -> None:
    """
    Generate and display waterfall charts for given LCIA indicator columns from a processed DataFrame.

    Parameters
    ----------
    processed_df : pd.DataFrame
        The DataFrame containing columns for various LCIA indicators (e.g., 'GWP', 'ADP', etc.)
        plus 'Process', 'Input/output', and 'Location'. Rows are typically LCA results.

    Notes
    -----
    - Uses Seaborn to build a color palette with a custom blend of Imperial-based colors.
    - Creates a separate Plotly waterfall bar chart for each LCIA indicator.
    - Displays each chart with .show().
    """

    # If the DataFrame is empty, there's nothing to plot
    if processed_df.empty:
        print("No data to plot. The DataFrame is empty.")
        return

    # Your custom or "Imperial" base colors (optionally tweak as needed)
    imperial_base_colors = ["#002147", "#0071A4", "#DA291C", "#F4A900", "#78BE20", "#7C878E"]

    # Generate a blended color scale using Seaborn
    color_scale = sns.color_palette(
        "blend:#002147,#0071A4,#DA291C,#F4A900,#78BE20,#7C878E",
        n_colors=10
    )
    hex_colors = [mcolors.to_hex(c) for c in color_scale]

    # Set a Seaborn style if desired
    sns.set_style("whitegrid")

    # Define the columns to plot and their Y-axis labels
    indicator_cols = [
        ('GWP',    'GWP (kg CO₂-eq)'),
        ('ADP',    'ADP (kg Sb-eq)'),
        ('Water use', 'Water Use (m³ eq. deprived)'),
        ('AP',     'AP (mol H⁺-eq)'),
        ('FETP',   'FETP (CTUe)'),
        ('HTP',    'HTP (CTUh)'),
        ('ODP',    'ODP (kg CFC-1-eq)'),
        ('PMFP',   'PMFP (kg PM2.5-eq)'),
        ('POFP',   'POFP (kg O₃-eq)')
    ]

    # Loop through each LCIA indicator and generate a waterfall chart
    for col, y_axis_title in indicator_cols:
        # Filter out NaN rows for this particular indicator and sort
        filtered_df = processed_df.dropna(subset=[col]).sort_values(by=col, ascending=False)
        if filtered_df.empty:
            print(f"No non-NaN data found for indicator '{col}'. Skipping chart.")
            continue

        processes = filtered_df['Process'].values
        inputs_outputs = filtered_df['Input/output'].values
        locations = filtered_df['Location'].values
        contributions = filtered_df[col].values

        total = contributions.sum()
        running_total = 0
        
        # Create a Plotly Figure (waterfall style by stacking bars)
        fig = go.Figure()

        # Build each bar in the waterfall
        for i, (process, value, io_label, location) in enumerate(zip(processes, contributions, inputs_outputs, locations)):
            numeric_text = format_numeric(value)
            hover_text = (
                f'Process: {process}<br>'
                f'Location: {location}<br>'
                f'{col}: {numeric_text}'
            )
            fig.add_trace(go.Bar(
                name=process,
                x=[io_label],
                y=[value],
                base=running_total,
                marker=dict(color=hex_colors[i % len(hex_colors)]),
                hovertext=hover_text,
                hoverinfo='text'
            ))
            running_total += value

        # Add a final bar for the total
        total_text_value = format_numeric(total)
        fig.add_trace(go.Bar(
            name="Total",
            x=["Total"],
            y=[total],
            marker=dict(color='gray', opacity=0.6),
            hovertext=f'Total: {total_text_value}',
            hoverinfo='text'
        ))

        # Styling the layout
        fig.update_layout(
            width=500,
            height=400,
            template="plotly_white",
            shapes=[
                dict(
                    type="rect",
                    xref="paper", yref="paper",
                    x0=0, y0=0, x1=1, y1=1,
                    line=dict(color="black", width=1),
                    fillcolor="rgba(0,0,0,0)"
                )
            ],
            font=dict(family="Arial", size=12, color="black"),
            margin=dict(l=60, r=20, t=20, b=60),
            showlegend=False
        )

        # Configure X-axis
        fig.update_xaxes(
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            ticks='inside',
            tickangle=45,
            tickfont=dict(size=12),
            showgrid=False
        )

        # Configure Y-axis
        fig.update_yaxes(
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            ticks='inside',
            tickfont=dict(size=12),
            gridcolor='rgba(200, 200, 200, 0.5)',
            zeroline=False,
            tickformat=".e",
            title=dict(
                text=y_axis_title,
                font=dict(size=14, color="black", family="Arial"),
            )
        )

        # Show the figure for this indicator
        fig.show()
