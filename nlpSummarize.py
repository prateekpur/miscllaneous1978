import pdfplumber
import nltk
import string
import numpy as np
import networkx as nx
import re
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

nltk.download('punkt')
model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 1: Extract text from the PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Step 2: Preprocess text (remove punctuation and lowercase)
def preprocess_text(text):
    # Remove punctuation and lower case the text
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    return text

# Step 3: Tokenize the text into sentences
def tokenize_sentences(text):
    return nltk.sent_tokenize(text)

# Step 4: Extract numbers using regex (common financial metrics)
def extract_financial_numbers(text):
    patterns = {
        "Total Assets": r"total assets[\s:\$]*([\d,]+\.?\d*)",
        "Total Revenue": r"total revenue[\s:\$]*([\d,]+\.?\d*)",
        "Net Income": r"net income[\s:\$]*([\d,]+\.?\d*)",
        "Total Liabilities": r"total liabilities[\s:\$]*([\d,]+\.?\d*)"
    }

    extracted_data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted_data[key] = match.group(1).replace(",", "")  # Remove commas for clean numbers
    return extracted_data

# Step 4: Extract keywords using TF-IDF
def extract_keywords(text, n_keywords=10):
    tfidf = TfidfVectorizer(stop_words='english', max_features=n_keywords)
    tfidf_matrix = tfidf.fit_transform([text])
    keywords = tfidf.get_feature_names_out()
    return keywords

# Step 5: Summarization using TextRank
def summarize_text(text, num_sentences=5):
    sentences = tokenize_sentences(text)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Compute similarity matrix
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Build graph
    graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(graph)

    # Rank sentences by importance
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    summary = " ".join([ranked_sentences[i][1] for i in range(min(num_sentences, len(ranked_sentences)))])
    
    return summary

def keyword_search(question, text):
    words = question.lower().split()
    for sent in sent_tokenize(text):
        if any(word in sent.lower() for word in words):
            return sent  # Return the first matching sentence
    return "I couldn't find an answer in the document."

def find_most_relevant_sentence(question, sentences):
    question_embedding = model.encode(question)
    sentence_embeddings = model.encode(sentences)

    # Find the most similar sentence
    similarities = util.cos_sim(question_embedding, sentence_embeddings)
    best_match_idx = similarities.argmax()
    return sentences[best_match_idx]



# Main workflow
pdf_path = "okta-last-quarter.pdf"  # Path to your PDF file


# Extract and preprocess text
extracted_text = extract_text_from_pdf(pdf_path)

#tokens = tokenize_sentences(extracted_text)
question = "Total assets"
sentences = tokenize_sentences(extracted_text)
#answer = keyword_search(question, extracted_text)
#print(answer)
answer = find_most_relevant_sentence(question, sentences)
print(answer)


#print(tokens)
#print(extract_financial_numbers(extracted_text))

# Generate a summary
# summary = summarize_text(extracted_text)

#print("Summary:")
# print(summary)