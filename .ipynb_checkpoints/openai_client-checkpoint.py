# openai_client.py

import openai
import os

def create_openai_client(api_key: str = None):
    """
    Creates and configures an OpenAI client using the provided API key.
    If no key is supplied, it attempts to load the key from the environment variable 'OPENAI_API_KEY'.

    Parameters
    ----------
    api_key : str, optional
        The OpenAI API key. If None, will look for OPENAI_API_KEY env variable.

    Returns
    -------
    openai
        The openai module with the API key set.
    """
    if api_key is None:
        # Option 1: Load from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("No API key found. Please set the OPENAI_API_KEY environment variable or pass api_key explicitly.")
    openai.api_key = api_key

    # Optionally, you could return something else if needed.
    # For now, we'll just return the openai module, so it's configured for immediate use.
    return openai
