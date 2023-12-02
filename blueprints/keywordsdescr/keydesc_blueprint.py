from flask import Flask, render_template, request, jsonify, Blueprint
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from collections import Counter

app = Flask(__name__)

# Create a Blueprint
keydesc_blueprint = Blueprint("keydesc_blueprint", __name__, template_folder="templates", static_url_path='/static')

def predict_keywords(text, threshold_frequency=3):
    # Convert text to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenize the text into words
    words = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]

    # Calculate word frequencies
    word_counts = Counter(filtered_words)

    # Select keywords
    keywords = [word for word, count in word_counts.items() if count > threshold_frequency]
    return keywords

@keydesc_blueprint.route('/keywordsdecsr')
def index():
    return render_template('index.html')

@keydesc_blueprint.route('/predict_keywords', methods=['POST'])
def predict_keywords_route():
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({"error": "Invalid request. 'text' parameter is missing."}), 400

        # Predict keywords using the model
        predicted_keywords = predict_keywords(text)

        # Return the predicted keywords
        return jsonify({"predicted_keywords": predicted_keywords})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# # Register the Blueprint with the app
# app.register_blueprint(keydesc_blueprint, url_prefix="/keywordsdecsr")

# if __name__ == "__main__":
#     app.run(debug=False,host='0.0.0.0')
