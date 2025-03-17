# search_utils.py

def build_search_query(term: str) -> str:
    """
    Constructs a wildcard search query from a term.
    E.g., "waste graphite" becomes "*waste* *graphite*".
    
    Parameters
    ----------
    term : str
        The search term to be expanded into a wildcard query.
    
    Returns
    -------
    str
        A wildcard query string suitable for partial matching.
    """
    terms = term.split()
    return "*" + "* *".join(terms) + "*"


def get_alternative_search_terms(client, search_term: str) -> list[str]:
    """
    Uses the ChatGPT API to suggest alternative search terms.
    
    Given an original search term (e.g., "waste graphite"), this function asks ChatGPT
    to provide a comma-separated list of alternative search terms that could capture similar datasets.
    
    Parameters
    ----------
    client : Any
        An OpenAI client object or module that's already been authenticated (e.g., openai).
    search_term : str
        The search term for which to generate alternative suggestions.
    
    Returns
    -------
    list[str]
        A list of alternative search terms suggested by the ChatGPT API.
    """
    prompt = (
        f"Suggest a list of 3 alternative search terms that could be used to find similar datasets "
        f"for the activity '{search_term}' in the ecoinvent database. Each suggestion should modify "
        f"the material name to represent similar materials. Return the suggestions as a comma-separated list."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides alternative search queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=50
        )
        suggestions_text = response.choices[0].message.content.strip()
        suggestions = [s.strip() for s in suggestions_text.split(',')]
        return suggestions
    except Exception as e:
        print("Error calling ChatGPT API:", e)
        return []
