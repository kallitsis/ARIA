[![Python application](https://github.com/kallitsis/ARIA/actions/workflows/python-app.yml/badge.svg)](https://github.com/kallitsis/ARIA/actions/workflows/python-app.yml)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)

# ARIA: Artificial Intelligence for Sustainability Assessment
 
ARIA is a Python package designed to streamline the rapid calculation of environmental impacts based on the Life Cycle Assessment (LCA) framework. By leveraging [Brightway2](https://github.com/brightway-lca) as its core infrastructure and integrating AI-based search and refinement, ARIA automates many of the tedious manual steps in inventory analysis—significantly reducing the time and expertise required for LCA studies.

ARIA comes with detailed [documentation](https://github.com/kallitsis/ARIA/wiki) and [examples](https://github.com/kallitsis/ARIA/tree/eb61f4a9ef608844cf783e6e5ca9ec34aadcf99a/examples). 

## Features

- **Automated Inventory Analysis:**  
  ARIA automatically matches user-supplied inputs with background datasets from Ecoinvent using natural language processing.
- **Brightway2 Integration:**  
  Provides a robust and reproducible LCA modelling environment.
- **AI-Powered Refinement:**  
  Uses the OpenAI API to generate search terms and select representaive background daasets based on detailed rules and contextual instructions.
- **Flexible Impact Assessment:**  
  Supports multiple impact assessment methods (default: EF v3.1) to calculate key environmental indicators such as global warming potential, acidification, and water use.
- **Visualisation:**  
  Generates plots and DataFrames for easy interpretation of results.
- **Modular Design:**  
  Structured into separate modules for project setup, data handling, search utilities, and processing, making it easy to extend and maintain.

## Installation

To install ARIA using `pip`, run the following command:

```bash
pip install ARIA
```

or clone it in your machine:

```bash
git clone https://github.com/kallitsis/aria.git
cd aria
pip install .
```

## Dependencies

In order to run ARIA, you will need an active [Ecoinvent license](https://ecoinvent.org/licenses/) and an [OpenAI API key](https://platform.openai.com/account/api-keys).
Go to [Purchasing OpenAI API Credits](https://github.com/kallitsis/ARIA/wiki/Purchasing-OpenAI-API-credits) to learn more about how to set this up. A full list of dependencies that will automatically be installed is shown [here](https://github.com/kallitsis/ARIA/wiki/Installation-steps).

## Quick start

To start using ARIA, you will need to [create a credentials.py](https://github.com/kallitsis/ARIA/wiki/Quick-start-guide) file which securely stores your Ecoinvent credentials and OpenAI API key to your local machine. Alternatively, you can set these up as environment variables.

For Linux/macOS:
```bash
export ECOINVENT_USERNAME="your_username"
export ECOINVENT_PASSWORD="your_password"
export OPENAI_API_KEY="your_api_key"
```
For Windows:
```powershell
$env:ECOINVENT_USERNAME="your_username"
$env:ECOINVENT_PASSWORD="your_password"
$env:OPENAI_API_KEY="your_api_key"
```

Once credentials are set, initialise the **Brightway2 project** and load the **Ecoinvent database** of your choice:
```python
from ARIA.project_setup import setup_brightway_project
project_name = "my brightway project"  # change this to your desired project name
ecoinvent_version = "3.10.1"           # change this to your preferred version
system_model = "cutoff"                # change this to "cutoff", "apos", or "consequential"
ecoinvent_db = setup_brightway_project(project_name, ecoinvent_version, system_model)
   ```

You will also need a **Data_inputs.xlsx** file which aggregates the life cycle inventory per functional unit in tabular format. The file should include four columns as default, **Input/output** listing any flows (activities), **In/out** listing the corresponding amount for each flow, **Units** in [default Ecoinvent format](https://eplca.jrc.ec.europa.eu/SDPDB/unitgroupList.xhtml;jsessionid=D0082C0606540373127C80107958A6E6?stock=default) and **Notes** providing any additional instructions for AI-based matching. Example files are shown [here](https://github.com/kallitsis/ARIA/tree/eb61f4a9ef608844cf783e6e5ca9ec34aadcf99a/examples).  
```python
from ARIA.data_handling import open_excel_with_applescript, read_and_clean_excel
file_path = "/path/to/your/file.xlsx"
data_frame = read_and_clean_excel(file_path)
```

With inventory data loaded and cleaned, you can initialise the OpenAI client and run the analysis to aytomatically match inventory flows with ecoinvent datasets.
```python
from ARIA.openai_client import create_openai_client
from credentials import OPENAI_API_KEY
from ARIA.search_workflow import process_dataframe

client = create_openai_client(OPENAI_API_KEY)

processed_df = process_dataframe(
    data_frame,
    db=ecoinvent_db,
    client=openai,
    system_message="You are an LCA domain expert. Please pick the best match.", #Optionally, add specific information related to your goal and scope definition or instructions on how to select datasets
    locations=["GLO", "RoW"] #Add any locations of focus based on Ecoinvent country codes
```
ARIA will return a dataframe with suggested Ecoinvent inventories for each flow. If they are representative, you can proceed with impact assessment and visualisation. 
```python
from ARIA.impact_assessment import run_impact_assessment
from ARIA.plot_lcia import plot_lcia_waterfall_charts

lcia_method = [ ... ]  # Define your methods, Environmental Footprint 3.1 default
processed_df = run_impact_assessment(processed_df, lcia_method)
plot_lcia_waterfall_charts(processed_df)
```
## Citing ARIA

If you use ARIA for a scientific paper, please cite our paper:
>placeholder

## License

ARIA is released under a [BSD 3-Clause License](LICENSE) and is fully open source.

## Contributing

When I make open source Insights>Community standards contributing guidelines, and code of conduct are requirements. 
