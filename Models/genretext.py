import requests
import pickle

API_KEY = "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"

def identify_genre(text, user_prompt):
    """Identifies a genre from text using the ChatGPT API.

    Args:
        text: The text for genre prediction.
        user_prompt: A user-defined prompt.

    Returns:
        A string representing the predicted genre.
    """

    url = "https://api.openai.com/v1/engines/davinci/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "prompt": f"{text} {user_prompt}?",
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

# Read the recognized text from the 'recognized.txt' file
with open('recognized.txt', 'r', encoding='utf-8') as file:
    recognized_text = file.read().split('\n')

user_prompt = "Categorize the Genre for these Keywords. give in one word Genre:"
predicted_genre = identify_genre(recognized_text, user_prompt)

# Display the predicted genre
print(f"The predicted genre is: {predicted_genre}")

# Save the identify_genre function to a pickle file
# file_path = "genretext.pkl"
# with open(file_path, 'wb') as file:
#     pickle.dump(identify_genre, file)
