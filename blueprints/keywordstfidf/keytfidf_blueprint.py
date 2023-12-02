# blueprints/keywordsdecsr/keywordsdecsr_blueprint.py
from flask import Blueprint, render_template, request, jsonify
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

keytfidf_blueprint = Blueprint("keytfidf_blueprint", __name__, template_folder="templates", static_url_path='/static')

@keytfidf_blueprint.route('/keywordstfidf')
def index():
    return render_template('index.html')
@keytfidf_blueprint.route("/predict_keywords", methods=["POST"])
def predict_keywords_tfidf():
    try:
        # Read text from "recognized.txt" file
        with open('recognized.txt', 'r', encoding='utf-8') as file:
            texts = [file.read()]

        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(texts)

        # Get feature names (words)
        feature_names = vectorizer.get_feature_names_out()

        # Convert TF-IDF matrix to DataFrame for better handling
        tfidf_df = pd.DataFrame(data=tfidf_matrix.toarray(), columns=feature_names)

        # Set a threshold for TF-IDF scores
        tfidf_threshold = 0.2  # You can adjust this threshold based on your preference

        # Filter out keywords based on the threshold
        relevant_keywords = tfidf_df.columns[tfidf_df.max() > tfidf_threshold]

        # Save relevant keywords in a .txt file
        output_file_path = "relevant_keywords.txt"
        with open(output_file_path, 'w') as file:
            file.write("\n".join(relevant_keywords))

        print("Relevant Keywords have been saved to:", output_file_path)

        # # Save the relevant_keywords variable to a pickle file
        # pickle_file_path = "keywords_tfidf.pkl"
        # with open(pickle_file_path, 'wb') as file:
        #     pickle.dump(relevant_keywords, file)

        return jsonify({"message": "Predicted and saved relevant keywords successfully."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
