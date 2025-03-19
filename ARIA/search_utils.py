# search_utils.py

def build_search_query(term: str, extra: str = "") -> str:
    """
    Constructs a wildcard search query from a term.
    E.g., "waste graphite" becomes "*waste* *graphite*". If extra content is provided,
    it appends those words to the search term.

    Parameters
    ----------
    term : str
        The search term to be expanded into a wildcard query.
    extra : str, optional
        Additional words to append to the search term.

    Returns
    -------
    str
        A wildcard query string suitable for partial matching.
    """
    terms = term.split()
    return "*" + "* *".join(terms) + "*"


def get_alternative_search_terms(client, search_term: str, extra_instructions: str = "") -> list[str]:
    """
    Uses the ChatGPT API to suggest alternative search terms.
    
    Given an original search term (e.g., "waste graphite"), this function asks ChatGPT
    to provide a comma-separated list of alternative search terms that could capture similar datasets.
    Additional instructions can be provided to further tailor the suggestions.
    
    Parameters
    ----------
    client : Any
        An OpenAI client object or module that's already been authenticated (e.g., openai).
    search_term : str
        The search term for which to generate alternative suggestions.
    extra_instructions : str, optional
        Additional instructions or context to refine the suggestions.
    
    Returns
    -------
    list[str]
        A list of alternative search terms suggested by the ChatGPT API.
    """
    prompt = (
        f"Suggest a list of 3 alternative search terms that could be used to find similar datasets \n"
        f"for the activity '{search_term}' in the ecoinvent database. Each suggestion should modify\n"
        f"the material name to represent similar materials and should be no more than two words.\n"
        f"for the activity '{search_term}'. If '{search_term}' includes the word production, maintain it in your suggesions and simply add a word.\n"
        f"Keep in mind that what you recommend will be used to find datasets in the Ecoinvent database for life cycle assessment, so your suggestions should be something that is likely to give matches.\n"
        f"Focus on alterntive matterials related to its composiion.\n"
        f"Return the suggestions as a comma-separated list."
    )
    if extra_instructions:
        prompt += f" {extra_instructions}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            presence_penalty=0.7,
            max_tokens=50
        )
        suggestions_text = response.choices[0].message.content.strip()
        suggestions = [s.strip() for s in suggestions_text.split(',')]
        return suggestions
    except Exception as e:
        print("Error calling ChatGPT API:", e)
        return []
