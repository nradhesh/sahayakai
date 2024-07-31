from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Load schemes from the CSV file
try:
    schemes_df = pd.read_csv("scheme_data.csv")
    schemes = schemes_df.apply(lambda x: x.to_string(), axis=1)
    print("Schemes loaded successfully.")
except Exception as e:
    print(f"Error loading schemes: {e}")

# Load the vectorizer from the pickle file
try:
    with open('Vector.pkl', 'rb') as file:
        vectorEmbeddings = pickle.load(file)
    vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer.fit(schemes)
    print("Vectorizer and embeddings loaded successfully.")
except Exception as e:
    print(f"Error loading vectorizer and embeddings: {e}")

def translate_keywords(keywords, target_language="en"):
    # Example translation logic
    translated_keywords = keywords
    return translated_keywords

def get_recommendations(user_keywords):
    try:
        if isinstance(user_keywords, str):
            user_keywords = [user_keywords]
        vec = vectorizer.transform(user_keywords)
        similarities = cosine_similarity(vec, vectorEmbeddings).flatten()
        top_indices = similarities.argsort()[-5:][::-1]
        recommendations = [schemes[i] for i in top_indices]
        print("Recommendations generated successfully.")
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

        translated_keywords = translate_keywords(keywords)
        print(f"Translated keywords: {translated_keywords}")

        recommendations = get_recommendations(translated_keywords)
        print("the recomendations are")
        print(recommendations)
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        print(f"Error in recommend endpoint: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5000)
    # print(get_recommendations('Scholarship'))