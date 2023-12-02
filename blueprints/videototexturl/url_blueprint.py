# blueprints/keywordsdecsr/keywordsdecsr_blueprint.py
from flask import Blueprint, render_template, request, jsonify
import os
url_blueprint = Blueprint("url_blueprint", __name__, template_folder="templates", static_url_path='/static')

# Function to process the video and extract keywords
def process_video_and_extract_keywords():
    # ... (rest of your code for processing the video and extracting keywords)

    # Replace the pickle loading with the actual code to extract keywords
    recognized_text_dict = {}  # Replace this with your actual logic to get recognized_text_dict

    return recognized_text_dict

# Uncomment the line below and run this script once to generate the recognized text dictionary
recognized_text_dict = process_video_and_extract_keywords()

@url_blueprint.route("/videototexturl")
def index():
    return render_template("index.html")

@url_blueprint.route("/predict_keywords", methods=["POST"])
def predict_keywords():
    try:
        data = request.get_json()
        chunk_number = data.get("chunk_number", "")
        
        if not chunk_number:
            return jsonify({"error": "Invalid request. 'chunk_number' parameter is missing."}), 400

        # Get recognized text for the specified chunk
        recognized_text = recognized_text_dict.get(f"chunk{chunk_number}", "")

        # Return the recognized text
        return jsonify({"recognized_text": recognized_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
