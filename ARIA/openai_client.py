#openai_client.py
import openai
import os

# Try to load the default API key from the environment variable first
default_api_key = os.getenv("OPENAI_API_KEY")

# If not set in environment, try to load from credentials.py
if default_api_key is None:
    try:
        from credentials import OPENAI_API_KEY as default_api_key
    except ImportError:
        default_api_key = None

def create_openai_client(api_key: str = None):
    """
    Creates and configures an OpenAI client using the provided API key.
    If no key is supplied, it first attempts to load the key from a local 
    credentials.py file, and if that fails, it will look for the OPENAI_API_KEY 
    environment variable.

    Parameters
    ----------
    api_key : str, optional
        The OpenAI API key. If None, the function will try to load it from 
        credentials.py or from the environment variable.

    Returns
    -------
    openai
        The openai module with the API key configured.
    """
    if api_key is None:
        if default_api_key:
            api_key = default_api_key
        else:
            api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "No API key found. Please set the OPENAI_API_KEY environment variable, "
                "include a credentials.py file with your key, or pass api_key explicitly."
            )
    openai.api_key = api_key
    return openai
