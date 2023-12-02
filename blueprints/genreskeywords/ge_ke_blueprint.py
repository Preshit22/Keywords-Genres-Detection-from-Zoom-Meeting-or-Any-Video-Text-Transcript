# from flask import Blueprint, render_template, request
# import joblib
# import numpy as np
# import pickle
# import requests

# ge_ke_blueprint = Blueprint("ge_ke_blueprint", __name__, template_folder="templates", static_url_path='/static')

# API_KEY = "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"

# def identify_genre(keywords, user_prompt):
#     """Identifies a genre from keywords using the ChatGPT API.

#     Args:
#         keywords: A list of keywords.
#         user_prompt: A user-defined prompt.

#     Returns:
#         A string representing the predicted genre.
#     """

#     # Join keywords into a comma-separated string
#     keywords_str = ', '.join(keywords)

#     url = "https://api.openai.com/v1/engines/davinci/completions"
#     headers = {
#         "Authorization": f"Bearer {API_KEY}"
#     }
#     data = {
#         "prompt": f"{keywords_str} {user_prompt}?",
#         "max_tokens": 100
#     }
#     response = requests.post(url, headers=headers, json=data)
#     response.raise_for_status()

#     # Check if the "choices" list is non-empty
#     choices = response.json().get("choices", [])
#     if choices:
#         # Extract the first word from the response
#         genre = choices[0]["text"].split()[0].strip()
#         return genre
#     else:
#         return "Genre prediction not available."

# @ge_ke_blueprint.route("/genreskeywords")
# def genreskeywords():
#     return render_template("index.html")

# @ge_ke_blueprint.route("/predict_genre", methods=["POST"])
# def predict_genre():
#     try:
#         # Get keywords from the form
#         keywords = request.form.get("keywords").split(',')
#         user_prompt = "categorize the genre for these keywords. give in one word genre."

#         # Predict genre using the model
#         predicted_genre = identify_genre(keywords, user_prompt)

#         # Render the result on the HTML page
#         return render_template("result.html", predicted_genre=predicted_genre)

#     except Exception as e:
#         return render_template("result.html", predicted_genre="Error predicting genre.")




from flask import Blueprint, render_template, request
import joblib
import numpy as np
import pickle
import requests

ge_ke_blueprint = Blueprint("ge_ke_blueprint", __name__, template_folder="templates", static_url_path='/static')

API_KEY = "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"

def identify_genre(keywords, user_prompt):
    # Same as before
    """Identifies a genre from keywords using the ChatGPT API.

    Args:
        keywords: A list of keywords.
        user_prompt: A user-defined prompt.

    Returns:
        A string representing the predicted genre.
    """

    # # Join keywords into a comma-separated string
    # keywords_str = ', '.join(text)

    url = "https://api.openai.com/v1/engines/davinci/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "prompt": f"{keywords} {user_prompt}?",
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

@ge_ke_blueprint.route("/genreskeywords")
def genreskeywords():
    return render_template("index.html")

@ge_ke_blueprint.route("/predict_genre", methods=["POST"])
def predict_genre():
    try:
        # Read keywords from the Python file
        with open("recognized.txt", "r") as file:
            recognized_text = file.read()
        user_prompt = "categorize the genre for these keywords. give in one-word genre."

        # Predict genre using the model
        predicted_genre = identify_genre(recognized_text, user_prompt)

        # Render the result on the HTML page
        return render_template("result.html", predicted_genre=predicted_genre)

    except Exception as e:
        return render_template("result.html", predicted_genre="Error predicting genre.")
