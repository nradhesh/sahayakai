import psycopg2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify

config = {
    'dbname': 'schemes',
    'user': 'postgres',
    'password': '#Shetty222',
    'host': 'localhost',
    'port': '5433'
}

app = Flask(__name__)

def connect_to_db():
    try:
        conn = psycopg2.connect(**config)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")

def fetch_schemes():
    conn = connect_to_db()
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM schemes")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows
        except psycopg2.Error as e:
            print(f"Error fetching schemes: {e}")
    else:
        print("Connection to database failed.")

def get_recommendations(user_keywords):
    schemes = fetch_schemes()
    if schemes is not None:
        scheme_data = [' '.join(map(str, scheme)) for scheme in schemes]

        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform(scheme_data + [user_keywords])

        cosine_sim = cosine_similarity(vectors[-1], vectors[:-1]).flatten()

        top_indices = cosine_sim.argsort()[-5:][::-1]
        top_schemes = [schemes[i] for i in top_indices]

        return top_schemes
    else:
        print("No schemes found in the database.")
        return []

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    user_keywords = data.get('keywords', '')
    recommendations = get_recommendations(user_keywords)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(port=5000)
