from .search_utils import build_search_query, get_alternative_search_terms
import pandas as pd

def process_dataframe(data_frame, db, client, user_message="", locations=None, verbose=False, 
                      llm_model="gpt-4o-mini", max_candidates=12):
    if locations is None:
        locations = ["GLO", "RoW"]

    # Ensure destination column exists
    if "Ecoinvent process" not in data_frame.columns:
        data_frame["Ecoinvent process"] = ""

    for index, row in data_frame.iterrows():
        activity_name = str(row["Input/output"]).strip().lower()
        note_text = str(row.get("Notes") or "").strip()

        if verbose:
            print(f"\nProcessing row {index + 1}: {activity_name}")

        initial_query = build_search_query(activity_name)

        # 1) Deterministic search
        search_results = []
        for location in locations:
            # If your bw2 doesn't support 'filter', do: db.search(...); then filter results by r['location'] == location
            search_results.extend(db.search(initial_query, limit=50, filter={"location": location}))

        # 2) If no results, try refined term from notes
        if not search_results and note_text:
            refined_prompt = (
                f"Based on the activity name '{activity_name}' and these instructions: '{note_text}',\n"
                f"provide a single refined search term of two words that best represents a dataset in the ecoinvent database."
            )
            refined_completion = client.chat.completions.create(
                model=llm_model,
                messages=[{"role": "user", "content": refined_prompt}],
                temperature=0.0,
                max_tokens=20,
            )
            refined_term = refined_completion.choices[0].message.content.strip()
            if verbose and refined_term:
                print("Refined term based on notes:", refined_term)

            if refined_term:
                refined_query = build_search_query(refined_term)
                for location in locations:
                    search_results.extend(db.search(refined_query, limit=50, filter={"location": location}))

        # 3) If still no results, ask for alternatives and try them
        if not search_results:
            alternatives = get_alternative_search_terms(client, activity_name, extra_instructions=note_text)
            if verbose and alternatives:
                print("LLM alternative terms:", alternatives)
            for alt_term in (alternatives or []):
                revised_query = build_search_query(alt_term)
                alt_results = []
                for location in locations:
                    alt_results.extend(db.search(revised_query, limit=50, filter={"location": location}))
                if alt_results:
                    search_results = alt_results
                    break

        # 4) If still empty, skip LLM selection to avoid hallucination
        if not search_results:
            if verbose:
                print("No candidates found after all attempts; leaving cell blank.")
            data_frame.at[index, "Ecoinvent process"] = ""
            continue

        # Early exit: if exactly one candidate, accept deterministically
        if len(search_results) == 1:
            chosen = search_results[0]["name"]
            if verbose:
                print("Single candidate found; selecting:", chosen)
            data_frame.at[index, "Ecoinvent process"] = chosen
            continue

        # 5) Build concise candidate list (top-N), then ask LLM to choose one by exact name
        #    Keep formatting strict to minimize ambiguity.
        trimmed = search_results[:max_candidates]
        results_lines = [f"{r['name']} | {r['location']} | {r.get('unit','')}" for r in trimmed]
        results_string = "\n".join(f"- {line}" for line in results_lines)

        prompt_content = (
            f"Given the user instructions: '{user_message}', help choose one dataset to be used for '{activity_name}' from the Ecoinvent database. Follow these rules:\n"
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

        chat_completion = client.chat.completions.create(
            model=llm_model,
            messages=[{"role": "user", "content": prompt_content}],
            temperature=0.0,
            max_tokens=50
        )
        response_content = chat_completion.choices[0].message.content.strip()
        if verbose:
            print("LLM selected:", response_content)

        data_frame.at[index, "Ecoinvent process"] = response_content

    return data_frame

    
