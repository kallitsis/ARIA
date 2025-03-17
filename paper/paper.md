---
title: 'ARIA: ARtificial Intelligence for sustainability Assessment'
tags:
    - Python
    - life cycle assessment
    - sustainability analysis
    - environmental impact
    - natural language processing
    - artificial intelligence
authors:
    - name: Evangelos Kallitsis
      orchid: 0000-0003-0948-3443
      affiliation: "1, 2"
affiliations:
    - name: Department of Mechanical Engineering, Imperial College London, United Kingdom
      index: 1
    - name: The Faraday Institution, United Kingdom
      index: 2
bibliography: paper.bib
---

# Summary
`ARIA` (ARtificial Intelligence for sustainability Assessment) is a Python package that allows the rapid calculation of the environmental impact of a product or process based on the life cycle assessment framework. In the sustainability analysis domain, researchers spend numerous hours trying to estimate the environmental impact of different inputs which are typically retrieved from databases, with the Ecoinvent database being by far the most widely used one (cite Ecoinvent). ARIA simplifies this process by utilising the OpenAI API (cite something) to automatically match input flows to background datasets from Ecoinvent ant perform impact assessment based on Brightway (cite brightway). The capability to process natural language enables the automatic selection of representative datasets corresponding to a product or process. 

# Statement of need
Life Cycle Assessment (LCA) is becoming an increasingly important method to analyse the environmental impact of products and processes (ref something LCA related). The methodology is described in the ISO14040/44 series of standards, detailing the four necessary steps to perform a reliable LCA: goal and scope definition, inventory analysis, impact assessment and interpretation. 

[insert figure about LCA stages and description]

Arguably, the most time consuming phase of an LCA is the inventory analysis phase, where practitioners write down all the inputs and outputs of a process and try to find datasets to represent them. For example, if a process uses electricity, the LCA practitioner needs to write down how much electricity is consumed by the process and try to find a dataset that represents the embodied environmental impact of the type of electricity that is supplied to the process. Given that numerous flows are typically associated with a product, matching background data to each one of them is a very time consuming step. 

In the LCA community, Brightway has emerged as the dominant open-source software to conduct an LCA. It provides flexibility and modularity, and seamlessly integrates with the Ecoinvent database. However, Brightway is more targeted towards the advanced LCA practitioner, presenting a high barrier to entry given that it is targeted towards users that are both experienced LCA practitioners and skilled coders. 

LCA is primarily a quantitative method used to evaluate the environmental impacts of a product's life cycle. However, LCA also has qualitative aspects that play a significant role in its application and interpretation. For example, during goal and scope definition the practitioner defines what is the geogrphical focus, the product under study and its technological dimensions. All this qualitative information will later influence the type of data that is used in inventory analysis. 

'ARIA' aims to reduce the barrier to entry for life cycle modelling. It was developed out of a need to perform rapid calculation of the environmental impact of battery recycling as part of the Faraday Institution ReLiB project, to guide process development in the lab.  Reduce the time of LCA inventory analysis from weeks to hours.
[expand on statement of need]

# ARIA Operating Principles
## Importing inventory data
'ARIA' has been developed to automate the calculation of environmental impacts associated with a product or process. The 


Therefore, the user needs to fill in the aggregate amount of inputs related to their product system per functional unit in the form of an xlsx spreadsheet 'data_inputs.xlsx'. This includes any mass and energy flows, transportation and facility requirements. Ideally, the units of each input should match the default Ecoinvent units, e.g. kg for mass, kWh for electricity, MJ for heat, a detailed list of them can be found here: (https://eplca.jrc.ec.europa.eu/SDPDB/unitgroupList.xhtml;jsessionid=D0082C0606540373127C80107958A6E6?stock=default).



Once the data are imported, a first scan is performed in the Ecoinvent database to find matching datasets for each flow, which are filtered based on user inpt and the geographical focus of the study. In the case that no results are found, the code asks ChatGPT to generate three alternative search terms associated to the text that the user inputted. While this is not a guarantee that a dataset will be found, it highly increases its likelihood. 

A refinement step is performed. Here, ChatGPT is prompted to go through all the datasets that were found for each flow, and select the most representative one. In doing so, some generic rules have been included (Figure 1) but the user is also free to fill in information related to their goal and scope definition, which would improve the refinement step overall. 

[Insert figure, snapshot how ChatGPT is prompted to refine datasets]

After some data processing, the dataframe containing all the necessary information associated with inventory analysis is printed. Next, the code utilises brightway to perform life cycle impact assessment. EF v3.1 has been used as the default impact assessment method, as it is the most up-to-date method (insert ref) but the user is flexible to change it to any method supported by brightway. The calculation of the environmental impact for each flow is then performed for all environmental impact categories and the results are plotted. 

[include a battery example]

## Example of Lithium-ion batteries
Use Kallitsis et al. (2024) BOM and compare results. 


## Limitations and future potential






