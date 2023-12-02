import requests

API_KEY = "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"

def identify_genre(keywords, user_prompt):
    """Identifies a genre from keywords using the ChatGPT API.

    Args:
        keywords: A list of keywords.
        user_prompt: A user-defined prompt.

    Returns:
        A string representing the predicted genre.
    """

    # Join keywords into a comma-separated string
    keywords_str = ', '.join(keywords)

    url = "https://api.openai.com/v1/engines/davinci/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "prompt": f"{keywords_str} {user_prompt}?",
        "max_tokens": 100
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    # Check if the "choices" list is non-empty
    choices = response.json().get("choices", [])
    if choices:
        # Extract the first word from the response
        genre = choices[0]["text"].split()[0].strip()
        return genre
    else:
        return "Genre prediction not available."

def read_keywords_from_file(file_path):
    """Reads keywords from a file.

    Args:
        file_path: Path to the file containing keywords.

    Returns:
        A list of keywords.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            keywords = file.read().split('\n')
            return [kw.strip() for kw in keywords if kw.strip()]
    except Exception as e:
        print(f"Error reading keywords from file: {str(e)}")
        return []

# Example usage:
user_prompt = "categorize the genre for above keywords. give in one word genre:"
keywords_file_path = "relevant_keywords.txt"
keywords = read_keywords_from_file(keywords_file_path)

# Filter out empty strings from the keywords
keywords = [kw for kw in keywords if kw.strip()]

predicted_genre = identify_genre(keywords, user_prompt)

# Display the predicted genre
print(f"The predicted genre is: {predicted_genre}")


# Save the identify_genre function to a pickle file
# file_path = "genre_keywords.pkl"
# with open(file_path, 'wb') as file:
#     pickle.dump(identify_genre, file)
