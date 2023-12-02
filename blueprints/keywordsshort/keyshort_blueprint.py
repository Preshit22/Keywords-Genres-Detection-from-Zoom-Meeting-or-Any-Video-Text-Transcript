from flask import Flask, render_template, request, jsonify, Blueprint
import re
import nltk
import pickle
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

keyshort_blueprint = Blueprint("keyshort_blueprint", __name__, template_folder="templates", static_url_path='/static')

# Use NLTK stopwords
stop_words = set(stopwords.words('english'))

def preprocess_text(txt):
    # Lower case
    txt = txt.lower()
    # Remove HTML tags
    txt = re.sub(r"<.*?>", " ", txt)
    # Remove special characters and digits
    txt = re.sub(r"[^a-zA-Z]", " ", txt)
    # Tokenization
    txt = nltk.word_tokenize(txt)
    # Remove stopwords
    txt = [word for word in txt if word not in stop_words]
    # Remove words less than three letters
    txt = [word for word in txt if len(word) >= 3]

    return " ".join(txt)

def get_keywords(recognized_text):
    recognized_text_preprocessed = preprocess_text(recognized_text)

    # Create a vocabulary and word count vectors
    cv = CountVectorizer(max_features=6000, ngram_range=(1, 2))
    word_count_vectors = cv.fit_transform([recognized_text])

    # Create a tf-idf transformer
    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(word_count_vectors)

    # Function to sort COO matrix
    def sort_coo(coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    # Function to extract top N items from a sorted COO matrix
    def extract_topn_from_vector(feature_names, sorted_items, topn=10):
        sorted_items = sorted_items[:topn]
        
        score_vals = []
        feature_vals = []
        for idx, score in sorted_items:
            fname = feature_names[idx]
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])
        
        results = {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]] = score_vals[idx]

        return results

    tf_idf_vector = tfidf_transformer.transform(cv.transform([recognized_text_preprocessed]))
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    keywords = extract_topn_from_vector(cv.get_feature_names_out(), sorted_items, 10)
    return list(keywords.keys())

@keyshort_blueprint.route('/keywordsshort')
def index():
    return render_template('index.html')

@keyshort_blueprint.route('/predict_keywords', methods=['POST'])
def predict_keywords_route():
    try:
        data = request.get_json()
        recognized_text = data.get('recognized_text', '')

        if not recognized_text:
            return jsonify({"error": "Invalid request. 'recognized_text' parameter is missing."}), 400

        # Predict keywords using the model
        keywords = get_keywords(recognized_text)

        # Return the predicted keywords
        return jsonify({"predicted_keywords": keywords})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app = Flask(__name__)
#     app.register_blueprint(keywords_short_blueprint, url_prefix="/keywords_short")
#     app.run(debug=True)
