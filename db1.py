# chatbot.py

import psycopg2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configuration for database connection
config = {
    'dbname': 'schemes',
    'user': 'postgres',
    'password': '#Shetty222',
    'host': 'localhost',
    'port': '5433'
}

def connect_to_db():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**config)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")

def fetch_schemes():
    """Fetches all schemes from the database."""
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
    """Returns top 5 schemes based on user provided keywords."""
    schemes = fetch_schemes()
    if schemes is not None:
        scheme_data = [' '.join(map(str, scheme)) for scheme in schemes]
        
        # Vectorize scheme data and user input using TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform(scheme_data + [user_keywords])
        
        # Calculate cosine similarity
        cosine_sim = cosine_similarity(vectors[-1], vectors[:-1]).flatten()
        
        # Get indices of top 5 schemes
        top_indices = cosine_sim.argsort()[-5:][::-1]
        top_schemes = [schemes[i] for i in top_indices]
        
        return top_schemes
    else:
        print("No schemes found in the database.")

def chatbot():
    """Runs the chatbot interface."""
    print("Welcome to the Government Schemes Recommender System!")
    user_input = input("Please enter keywords related to the scheme you are looking for: ")
    recommendations = get_recommendations(user_input)
    
    if recommendations:
        print("\nTop 5 Schemes:")
        for scheme in recommendations:
            print(f"Scheme Name: {scheme[0]}")
            print(f"Details: {scheme[1]}")
            print(f"Benefits: {scheme[2]}")
            print(f"Eligibility: {scheme[3]}")
            print(f"Exclusion: {scheme[4]}")
            print(f"Application Procedure: {scheme[5]}")
            print(f"Documents Required: {scheme[6]}")
            print(f"FAQ: {scheme[7]}")
            print(f"Link: {scheme[8]}")
            print(f"Keywords: {scheme[9]}\n")
    else:
        print("No recommendations found.")

if __name__ == "__main__":
    chatbot()
