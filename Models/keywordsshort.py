import re
import nltk
import pickle
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# Read the recognized text from the 'recognized.txt' file
with open('recognized.txt', 'r', encoding='utf-8') as file:
    recognized_text = file.read()

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

# Create a vocabulary and word count vectors
cv = CountVectorizer(max_features=6000, ngram_range=(1, 2))
word_count_vectors = cv.fit_transform([recognized_text])

# Create a tf-idf transformer
tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(word_count_vectors)

def get_keywords(recognized_text, cv, tfidf_transformer):
    recognized_text_preprocessed = preprocess_text(recognized_text)
    tf_idf_vector = tfidf_transformer.transform(cv.transform([recognized_text_preprocessed]))
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    keywords = extract_topn_from_vector(cv.get_feature_names_out(), sorted_items, 10)
    return keywords

def print_and_save_results(keywords):
    print("\n===Keywords===")
    for k in keywords:
        if not k.isdigit():
            print(k)

    with open('relevant_keywords.txt', 'w', encoding='utf-8') as file:
        for k in keywords:
            if not k.isdigit():
                file.write(f"{k}\n")

# Get keywords, print the results, and save to relevant_keywords.txt
keywords = get_keywords(recognized_text, cv, tfidf_transformer)
print_and_save_results(keywords)

# Save the get_keywords function to a pickle file
file_path = "keywords_short.pkl"
with open(file_path, 'wb') as file:
    pickle.dump(get_keywords, file)
