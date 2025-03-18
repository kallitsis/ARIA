# project_setup.py

try:
    import brightway2 as bw
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(
        "Brightway2 is not installed. Please run 'pip install brightway2' in your environment."
    ) from e

# Import confidential credentials from a local file.
try:
    from credentials import ECOINVENT_USERNAME, ECOINVENT_PASSWORD
except ImportError:
    raise ImportError("Please create a 'credentials.py' file with your confidential keys.")

def setup_brightway_project(
    project_name: str,
    ecoinvent_version: str,
    system_model: str,
    username: str = None,
    password: str = None
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
        The system model for the ecoinvent release (e.g., 'cutoff', 'apos', 'consequential').
    username : str, optional
        Ecoinvent username. If None, the value from credentials.py is used.
    password : str, optional
        Ecoinvent password. If None, the value from credentials.py is used.

    Returns
    -------
    bw.Database
        The Brightway2 database object for the imported (or existing) ecoinvent DB.
    """
    # Use credentials from credentials.py if none provided.
    if username is None:
        username = ECOINVENT_USERNAME
    if password is None:
        password = ECOINVENT_PASSWORD

    # Set the current project (creates it if it doesn't exist)
    bw.projects.set_current(project_name)
    
    # Perform basic Brightway2 setup
    bw.bw2setup()

    # Construct the ecoinvent database name
    ecoinvent_db_name = f"ecoinvent-{ecoinvent_version}-{system_model}"

    # Check if this ecoinvent database already exists
    if ecoinvent_db_name in bw.databases:
        print(f"'{ecoinvent_db_name}' is already present in the project '{project_name}'.")
    else:
        # If not, import the ecoinvent release using the provided credentials
        bw.import_ecoinvent_release(
            version=ecoinvent_version,
            system_model=system_model,
            username=username,
            password=password
        )
        print(f"'{ecoinvent_db_name}' has been imported into the project '{project_name}'.")

    # Return the database object for further use
    return bw.Database(ecoinvent_db_name)

