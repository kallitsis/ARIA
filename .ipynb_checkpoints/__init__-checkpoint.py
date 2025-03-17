# __init__.py

from ._version_ import __version__

# Import and optionally re-export relevant functions from each module.

from .project_setup import setup_brightway_project
from .data_handling import open_excel_with_applescript, read_and_clean_excel
from .search_utils import build_search_query, get_alternative_search_terms
from .search_workflow import process_dataframe
from .ecoinvent_processing import process_ecoinvent_dataframe
from .impact_assessment import run_impact_assessment
from .plot_lcia import plot_lcia_waterfall_charts

__all__ = [
    "setup_brightway_project",
    "open_excel_with_applescript",
    "read_and_clean_excel",
    "build_search_query",
    "get_alternative_search_terms",
    "process_dataframe",
    "process_ecoinvent_dataframe",
    "run_impact_assessment",
    "plot_lcia_waterfall_charts",
    "__version__",
]
