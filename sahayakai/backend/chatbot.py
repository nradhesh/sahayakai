from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import google.generativeai as genai
import psycopg2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# config = {
#     'dbname': 'schemes',
#     'user': 'postgres',
#     'password': '#Shetty222',
#     'host': 'localhost',
#     'port': '5433'
# }

app = Flask(__name__)
CORS(app)

def connect_to_db():
    # try:
    #     conn = psycopg2.connect(**config)
    #     return conn
    # except psycopg2.Error as e:
    #     print(f"Error connecting to PostgreSQL database: {e}")
    global df 
    df = pd.read_csv("scheme_data.csv")
    global embedding 
    embedding = None
    with open("Vector.pkl", "rb") as f:
        embedding = pickle.load(f)
    genai.configure(api_key="AIzaSyAHZtgC-fHXDveWo0rzAEm4HaMGNAGVyVQ")
    global model 
    model = genai.GenerativeModel('gemini-1.5-flash')
    global vectorizer 
    vectorizer = TfidfVectorizer(stop_words='english')
    con = df.apply(lambda x:x.to_string(), axis=1)
    vectorizer.fit(con)

# def fetch_schemes():
#     conn = connect_to_db()
#     if conn is not None:
#         try:
#             cur = conn.cursor()
#             cur.execute("SELECT * FROM schemes")
#             rows = cur.fetchall()
#             cur.close()
#             conn.close()
#             return rows
#         except psycopg2.Error as e:
#             print(f"Error fetching schemes: {e}")
#     else:
#         print("Connection to database failed.")

def get_recommendations(user_keywords):
    # schemes = fetch_schemes()

    # if schemes is not None:
    #     scheme_data = [' '.join(map(str, scheme)) for scheme in schemes]

    #     vectorizer = TfidfVectorizer(stop_words='english')
    #     vectors = vectorizer.fit_transform(scheme_data + [user_keywords])

    #     cosine_sim = cosine_similarity(vectors[-1], vectors[:-1]).flatten()

    #     top_indices = cosine_sim.argsort()[-5:][::-1]
    #     top_schemes = [schemes[i] for i in top_indices]

    #     print(f"Recommendations: {top_schemes}")  # Add logging here
    #     return top_schemes
    # else:
    #     print("No schemes found in the database.")
    #     return []

    vec = vectorizer.transform(user_keywords)
    # nfeatures = embedding.shape[1]
    # Ensure user_vec has the same number of features as self.embedding
    # if vec.shape[1] < nfeatures:
    #     user_vec = np.pad(vec.toarray(), ((0, 0), (0, nfeatures - vec.shape[1])), 'constant')
    # else:
    user_vec = vec.toarray()
    cosine_sim = cosine_similarity(embedding, user_vec).flatten()
    top_indices = cosine_sim.argsort()[-5:][::-1]
    top_schemes = [df.iloc[i] for i in top_indices]

    return top_schemes

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    user_keywords = data.get('keywords', '')
    print(f"Received keywords: {user_keywords}")  # Add logging here
    recommendations = get_recommendations(user_keywords)
    print(f"Sending recommendations: {recommendations}")  # Add logging here
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(port=5000)