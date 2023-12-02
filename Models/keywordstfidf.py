from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle

# Read text from "recognized.txt" file
with open('Generated Text/recognized.txt', 'r', encoding='utf-8') as file:
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

# Store relevant keywords in a .txt file
output_file_path = "relevant_keywords.txt"
with open(output_file_path, 'w') as file:
    file.write("\n".join(relevant_keywords))

print("Relevant Keywords have been saved to:", output_file_path)

# Save the relevant_keywords variable to a pickle file
pickle_file_path = "keywords_tfidf.pkl"
with open(pickle_file_path, 'wb') as file:
    pickle.dump(relevant_keywords, file)
