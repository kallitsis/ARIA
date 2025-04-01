[![Python application](https://github.com/kallitsis/ARIA/actions/workflows/python-app.yml/badge.svg)](https://github.com/kallitsis/ARIA/actions/workflows/python-app.yml)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/kallitsis/ARIA)

# **ARIA**: **AR**tificial **I**ntelligence for Sustainability **A**ssessment 

ARIA is a Python package designed to streamline the rapid calculation of environmental impacts based on the Life Cycle Assessment (LCA) framework. By leveraging Brightway2 as its core infrastructure and integrating AI-based search and refinement, ARIA automates many of the tedious manual steps in inventory analysis—significantly reducing the time and expertise required for LCA studies.

## Overview

- **Automated Inventory Analysis:**  
  ARIA automatically matches user-supplied inputs with background datasets (e.g., from Ecoinvent) using natural language processing.
- **Brightway2 Integration:**  
  Provides a robust and reproducible LCA modelling environment.
- **AI-Powered Refinement:**  
  Uses the OpenAI API to generate search terms and select representaive background daasets based on detailed rules and contextual instructions.
- **Flexible Impact Assessment:**  
  Supports multiple LCIA methods (default: EF v3.1) to compute key environmental indicators such as global warming potential, acidification, and water use.
- **Visualisation:**  
  Generates plots and DataFrames for easy interpretation of results.
- **Modular Design:**  
  Structured into separate modules for project setup, data handling, search utilities, and processing, making it easy to extend and maintain.

## Installation

ARIA is released under the [BSD 3-Clause License] license and is open source. To install ARIA, clone the repository and install it in editable mode:

```bash
git clone https://github.com/kallitsis/ARIA.git
cd ARIA
pip install -e .
