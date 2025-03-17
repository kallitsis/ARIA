# search_workflow.py

from search_utils import build_search_query, get_alternative_search_terms

def process_dataframe(data_frame, db, client):
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

    Returns
    -------
    pd.DataFrame
        The same data_frame, updated with ChatGPT recommendations 
        in the 'Ecoinvent process' column.
    """
    # Define the locations you want to filter
    locations = ["GLO", "RoW", "GB"]

    # Iterate over each row in the DataFrame
    for index, row in data_frame.iterrows():
        # 1) Get the full sentence (activity name) from the current row
        activity_name = row["Input/output"].strip().lower()  # ensure lowercase
        print(f"\nProcessing row {index + 1}: {activity_name}")

        # 2) Build initial wildcard query
        initial_query = build_search_query(activity_name)

        # 3) Search the database
        search_results = []
        for location in locations:
            search_results.extend(
                db.search(initial_query, limit=50, filter={"location": location})
            )

        # 4) Evaluate search results
        results_string = ""
        if search_results:
            print(f"Found {len(search_results)} matching activities for '{activity_name}':")
            for result in search_results:
                results_string += f"- {result['name']}, {result['location']}, {result['unit']} \n"
            print(results_string)
        else:
            print(f"No matching activities found for '{activity_name}'.")

            # 5) Ask ChatGPT for alternative terms
            alternative_terms = get_alternative_search_terms(client, activity_name)
            if alternative_terms:
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
                        print(f"\nFound {len(alternative_results)} matching activities for alternative search term '{alt_term}':")
                        results_string = ""
                        for result in alternative_results:
                            results_string += f"- {result['name']}, {result['location']}\n"
                        print(results_string)
                        found_alternative = True
                        break
                if not found_alternative:
                    print("No matching datasets found even after trying ChatGPT suggestions.")
            else:
                print("No alternative search term suggestions were received from ChatGPT.")

        # 6) Ask ChatGPT to choose which dataset to use
        # (If results_string is empty, ChatGPT sees an empty list of results.)
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        # Provide context: product system info, type of LCA, geographic boundary, etc.
                        "\n"  # Example: placeholders
                        "\n"
                        "\n"
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"The Ecoinvent database found the following results:\n'{results_string}'\n"
                        f"related to '{activity_name}'.\n"
                        f"Choose one dataset to be used for '{activity_name}' under the following rules:\n"
                        f"1. If they exist, give highest preference to datasets that include the exact term '{activity_name}'.\n"
                        f"2. Print only the exact name of the recommended dataset as shown in '{results_string}' (no extra text).\n"
                        f"3. Always give preference to datasets that match the exact terms in '{activity_name}'.\n"
                        f"4. If '{activity_name}' includes 'production', do not choose a dataset that includes 'waste'.\n"
                        f"5. If '{activity_name}' includes 'waste', do not choose a dataset that includes 'production'; prefer 'treatment'.\n"
                        f"6. If '{activity_name}' includes 'electricity', prefer 'market group for electricity, medium voltage'.\n"
                    )
                }
            ],
            temperature=0.7,
            max_tokens=50
        )
        # Extract ChatGPT's chosen dataset
        response_content = chat_completion.choices[0].message.content.strip()
        print("ChatGPT Response:")
        print(response_content)

        # Save the ChatGPT response in the 'Ecoinvent process' column
        data_frame.at[index, "Ecoinvent process"] = response_content

    return data_frame
