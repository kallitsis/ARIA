# project_setup.py

import brightway2 as bw

def setup_brightway_project(
    project_name: str,
    ecoinvent_version: str = "3.10.1",
    system_model: str = "cutoff",
    username: str = "ICL",
    password: str = "ICL_2019-20"
):
    """
    Set up the Brightway2 project environment, run bw2setup, 
    and (if needed) import the specified ecoinvent database.

    Parameters
    ----------
    project_name : str
        Name of the Brightway2 project to create or load.
    ecoinvent_version : str
        Ecoinvent version to import (e.g., '3.10.1').
    system_model : str
        The system model for the ecoinvent release (cutoff/apos/consequential).
    username : str
        Ecoinvent username.
    password : str
        Ecoinvent password.

    Returns
    -------
    bw.Database
        The Brightway2 database object for the imported (or existing) ecoinvent DB.
    """
    # Set the current project (creates it if it doesn't exist)
    bw.projects.set_current(project_name)
    
    # Ensure basic Brightway2 setup is performed
    bw.bw2setup()

    # Construct the ecoinvent database name
    ecoinvent_db_name = f"ecoinvent-{ecoinvent_version}-{system_model}"

    # Check if this ecoinvent database already exists
    if ecoinvent_db_name in bw.databases:
        print(f"'{ecoinvent_db_name}' is already present in the project '{project_name}'.")
    else:
        # If not, import it
        bw.import_ecoinvent_release(
            version=ecoinvent_version,
            system_model=system_model,
            username=username,
            password=password
        )
        print(f"'{ecoinvent_db_name}' has been imported into the project '{project_name}'.")
    
    # Return the database object for further use
    return bw.Database(ecoinvent_db_name)
