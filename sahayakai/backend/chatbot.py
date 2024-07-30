from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import pandas as pd
import pickle

app = Flask(__name__)
CORS(app)

# Load schemes from the CSV file
schemes_df = pd.read_csv("scheme_data.csv")
schemes = schemes_df.apply(lambda x:x.to_string(), axis=1)

# Load the vectorizer from the pickle file
with open('vector.pkl', 'rb') as file:
    vectorEmbeddings = pickle.load(file)
vectorizer = TfidfVectorizer(stop_words='english')
vectorizer.fit(schemes)


def translate_keywords(keywords, target_language="en"):
    """
    Translate keywords to the target language using an external translation API.
    For this example, we'll assume the keywords are already in the target language.
    """
    # Example translation logic, assuming the keywords are already in English
    translated_keywords = keywords
    return translated_keywords

def get_recommendations(user_keywords):
    try:
        # Ensure user_keywords is a list for vectorizer.transform
        if isinstance(user_keywords, str):
            user_keywords = [user_keywords]

        # Transform the user keywords into the same vector space as the descriptions
        vec = vectorizer.transform(user_keywords)
        # Calculate the cosine similarity between the user keywords and all scheme descriptions
        similarities = cosine_similarity(vec, vectorEmbeddings).flatten()
        # Get the indices of the top 5 most similar schemes
        top_indices = similarities.argsort()[-5:][::-1]
        # Get the corresponding schemes
        recommendations = [schemes[i] for i in top_indices]
        print(recommendations)
        return recommendations
    except Exception as e:
        print(f"Error in get_recommendations: {e}")
        return []

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        keywords = data.get('keywords', '')
        print(f"Received keywords: {keywords}")

        # Translate keywords to English
        translated_keywords = translate_keywords(keywords)
        print(f"Translated keywords: {translated_keywords}")

        # Get recommendations
        recommendations = get_recommendations(translated_keywords)
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        print(f"Error in recommend endpoint: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

if __name__ == '__main__':
    app.run(debug=False)
