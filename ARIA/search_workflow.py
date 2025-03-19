from .search_utils import build_search_query, get_alternative_search_terms
import pandas as pd

def process_dataframe(
    data_frame, 
    db, 
    client, 
    user_message="", 
    locations=None,
    verbose=False
):
    """
    Loop over rows in the data_frame, search the Ecoinvent database,
    optionally query ChatGPT for refined or alternative terms, and fill an 
    'Ecoinvent process' column with a recommended dataset.

    Parameters
    ----------
    data_frame : pd.DataFrame
        A DataFrame that must have at least one column 'Input/output'
        for the activity name. Optionally, it may include a 'Notes' column.
    db : brightway2.Database
        The Ecoinvent database object or equivalent for searching.
    client : Any
        An OpenAI-like client that can make chat completion calls 
        (e.g., openai with an API key set).
    user_message : str, optional
        Additional instructions provided by the user for refining dataset selection.
    locations : list of str, optional
        A list of location codes to filter when searching the database.
        Defaults to ["GLO", "RoW"] if not provided.
    verbose : bool, optional
        If True, prints detailed intermediate output; if False, suppresses
        intermediate printing.

    Returns
    -------
    pd.DataFrame
        The updated DataFrame with ChatGPT recommendations in the 
        'Ecoinvent process' column.
    """
    if locations is None:
        locations = ["GLO", "RoW"]

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
            # -----------------------
            # Step 1: If notes exist, try generating a refined term.
            refined_term = ""
            if "Notes" in data_frame.columns:
                note_text = row.get("Notes", "").strip()
                if note_text:
                    refined_prompt = (
                        f"Based on the activity name '{activity_name}' and these instructions: '{note_text}', /n"
                        f"provide a single refined search term of two words that best represents a dataset in the ecoinvent database."
                    )
                    refined_completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": refined_prompt}],
                        temperature=0.7,
                        max_tokens=20
                    )
                    refined_term = refined_completion.choices[0].message.content.strip()
                    if verbose:
                        print("Refined term based on notes:", refined_term)
                    if refined_term:
                        refined_query = build_search_query(refined_term)
                        refined_results = []
                        for location in locations:
                            refined_results.extend(
                                db.search(refined_query, limit=50, filter={"location": location})
                            )
                        if refined_results:
                            if verbose:
                                print(f"Found {len(refined_results)} matches using the refined term '{refined_term}'.")
                            search_results = refined_results
                            # Update results_string based on refined_results.
                            results_string = ""
                            for result in refined_results:
                                results_string += f"- {result['name']}, {result['location']}, {result.get('unit', '')}\n"
            
            # -----------------------
            # Step 2: If still no matches, ask ChatGPT for alternative search terms.
            if not search_results:
                extra_instructions = ""
                if "Notes" in data_frame.columns:
                    note_text = row.get("Notes", "").strip()
                    if note_text:
                        extra_instructions = note_text
                if user_message:
                    extra_instructions = (extra_instructions + " " + user_message).strip() if extra_instructions else user_message.strip()
                
                alternative_terms = get_alternative_search_terms(client, activity_name, extra_instructions=extra_instructions)
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
                            search_results = alternative_results
                            break
                    if not found_alternative and verbose:
                        print("No matching datasets found even after trying ChatGPT suggestions.")
                else:
                    if verbose:
                        print("No alternative search term suggestions were received from ChatGPT.")

        # -----------------------
        # Build the complete prompt for ChatGPT using the (possibly refined) results_string.
        prompt_content = (
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
            f"8. If '{activity_name}' does not include the term 'waste', never choose a dataset that includes this term or 'treatment'.\n"
            f"9. If '{activity_name}' does not include the term 'electricity', never choose a dataset that includes the exact term 'electricity'.\n"
        )


        # Ask ChatGPT to choose which dataset to use based on the prompt.
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt_content}
            ],
            temperature=0.7,
            max_tokens=50
        )
        response_content = chat_completion.choices[0].message.content.strip()
        if verbose:
            print("ChatGPT Response:")
            print(response_content)
        data_frame.at[index, "Ecoinvent process"] = response_content



  #  if verbose:
  #      print(f"\nARIA refined {refined_count} datasets. Final results:")
  #      print(data_frame.to_string(index=False))
    
    return data_frame

    
