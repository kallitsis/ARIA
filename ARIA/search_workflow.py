from .search_utils import build_search_query, get_alternative_search_terms

def process_dataframe(
    data_frame, 
    db, 
    client, 
    system_message="", 
    locations=None,
    verbose=False
):
    """
    Loop over rows in the data_frame, search the Ecoinvent database,
    optionally query ChatGPT for alternative terms, and fill an 
    'Ecoinvent process' column with a recommended dataset.

    Parameters
    ----------
    data_frame : pd.DataFrame
        A DataFrame that must have at least one column 'Input/output'
        for the activity name.
    db : brightway2.Database
        The Ecoinvent database object or equivalent for searching.
    client : Any
        An OpenAI-like client that can make chat completion calls 
        (e.g., openai with an API key set).
    system_message : str, optional
        Custom text to provide context for the ChatGPT "system" role.
    locations : list of str, optional
        A list of location codes to filter when searching the database.
        Defaults to ["GLO", "RoW", "GB"] if not provided.
    verbose : bool, optional
        If True, prints detailed intermediate output. If False, suppresses printing
        except for a final summary of refined datasets and results.

    Returns
    -------
    pd.DataFrame
        The updated DataFrame with ChatGPT recommendations in the 
        'Ecoinvent process' column.
    """
    if locations is None:
        locations = ["GLO", "RoW"]

    refined_count = 0  # Count how many datasets are refined

    for index, row in data_frame.iterrows():
        activity_name = row["Input/output"].strip().lower()
        if verbose:
            print(f"\nProcessing row {index + 1}: {activity_name}")
        initial_query = build_search_query(activity_name)
        
        # Search the database for each location.
        search_results = []
        for location in locations:
            search_results.extend(
                db.search(initial_query, limit=50, filter={"location": location})
            )

        results_string = ""
        if search_results:
            if verbose:
                print(f"Found {len(search_results)} matching activities for '{activity_name}':")
            for result in search_results:
                results_string += f"- {result['name']}, {result['location']}, {result.get('unit', '')}\n"
            if verbose:
                print(results_string)
        else:
            if verbose:
                print(f"No matching activities found for '{activity_name}'.")
            # Ask ChatGPT for alternative terms.
            alternative_terms = get_alternative_search_terms(client, activity_name)
            if alternative_terms:
                if verbose:
                    print("ChatGPT suggested the following alternative search terms:", alternative_terms)
                found_alternative = False
                for alt_term in alternative_terms:
                    revised_query = build_search_query(alt_term)
                    alternative_results = []
                    for location in locations:
                        alternative_results.extend(
                            db.search(revised_query, limit=50, filter={"location": location})
                        )
                    if alternative_results:
                        if verbose:
                            print(f"Found {len(alternative_results)} matching activities for alternative search term '{alt_term}':")
                        results_string = ""
                        for result in alternative_results:
                            results_string += f"- {result['name']}, {result['location']}\n"
                        if verbose:
                            print(results_string)
                        found_alternative = True
                        break
                if not found_alternative and verbose:
                    print("No matching datasets found even after trying ChatGPT suggestions.")
            else:
                if verbose:
                    print("No alternative search term suggestions were received from ChatGPT.")

        # Ask ChatGPT to choose which dataset to use using the detailed rules.
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message or ""},
                {"role": "user", "content": (
                    f"The Ecoinvent database found the following results:\n'{results_string}'\n"
                    f"related to '{activity_name}'.\n"
                    f"Choose one dataset to be used for '{activity_name}' under the following rules:\n"
                    f"1. If they exist, give highest preference to datasets that include the exact term '{activity_name}'.\n"
                    f"2. Print only the exact name of the recommended dataset as shown in '{results_string}' (no extra text).\n"
                    f"3. Always give preference to datasets that match the exact terms in '{activity_name}'.\n"
                    f"4. If '{activity_name}' includes 'production', do not choose a dataset that includes 'waste'.\n"
                    f"5. If '{activity_name}' includes 'waste', do not choose a dataset that includes 'production'; prefer 'treatment'.\n"
                    f"6. If '{activity_name}' includes 'electricity', prefer datasets that include the exact term 'market group for electricity, medium voltage'.\n"
                    f"7. Only print the name of the dataset as it was found in Ecoinvent, without any extra text.\n"
                    f"8. If '{activity_name}' does not include the term 'waste', never a dataset that includes this term or 'treatment'.\n"
                    f"9. If '{activity_name}' does not include the term 'electricity', never choose a datasets that include the exact term 'electricity'"
                    
                )}
            ],
            temperature=0.7,
            max_tokens=50
        )
        response_content = chat_completion.choices[0].message.content.strip()
        if verbose:
            print("ChatGPT Response:")
            print(response_content)
        data_frame.at[index, "Ecoinvent process"] = response_content

        if response_content:
            refined_count += 1
    
    return data_frame
    
