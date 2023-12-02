import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import pickle
from collections import Counter  # Add this import


# Read the text from the 'recognized.txt' file
with open(r'recognized.txt', 'r', encoding='utf-8') as file:
    text = file.read()

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

# Select keywords (adjust the threshold as needed)
threshold_frequency = 3
keywords = [word for word, count in word_counts.items() if count > threshold_frequency]

# Display or save keywords
print(keywords)

# Save the keywords list to a pickle file
# file_path = "keywordsdescr.pkl"
# with open(file_path, 'wb') as file:
#     pickle.dump(keywords, file)
