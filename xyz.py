import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import google.generativeai as genai

class ChatBot:

    recommendation_examples = [
        "I need a scholarship for college. I'm a girl and my family doesn't make much money.",
        "I'm a farmer living in a village. I want to start a small business. What government schemes can help me?",
        "I'm out of work and need training programs. Are there any government schemes I can use?",
        "I run a small shop and need some financial support. What grants can I apply for?"
    ]
    information_examples = [
        "What are the eligibility criteria for the XYZ scholarship?",
        "Can you tell me the benefits of the ABC startup scheme?",
        "What documents do I need to apply for the DEF financial aid?",
        "How do I sign up for the GHI job training program?"
    ]

    def __init__(self):
        self.df = pd.read_csv("scheme_data.csv")
        with open("Vector.pkl", "rb") as f:
            self.embedding = pickle.load(f)
        genai.configure(api_key="AIzaSyAHZtgC-fHXDveWo0rzAEm4HaMGNAGVyVQ")
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        # Fit vectorizer on dataset
        self.vectorizer = TfidfVectorizer(stop_words='english')
        combined_text = (self.df['SchemeName'] + " " + self.df['Details'] + " " + 
                         self.df['Benefits'] + " " + self.df['Eligibility']).fillna('')
        self.vectorizer.fit(combined_text)
        self.embedding = self.vectorizer.transform(combined_text)

    def get_recommendations(self, prompt):
        # Transform prompt using the fitted vectorizer
        vec = self.vectorizer.transform([prompt])
        nfeatures = self.embedding.shape[1]
        # Ensure user_vec has the same number of features as self.embedding
        if vec.shape[1] < nfeatures:
            user_vec = np.pad(vec.toarray(), ((0, 0), (0, nfeatures - vec.shape[1])), 'constant')
        else:
            user_vec = vec.toarray()

        cosine_sim = cosine_similarity(self.embedding, user_vec).flatten()
        top_indices = cosine_sim.argsort()[-5:][::-1]
        top_schemes = [self.df.iloc[i]['SchemeName'] for i in top_indices]

        return top_schemes

    def get_prompt(self):
        prompt = input("Enter prompt: ")
        keyword_prompt = f"Extract only keywords from this for making cosine similarity with our database: {prompt}. Give only keywords separated by space. Don't explain, don't put hyphen."
        response = self.model.generate_content(keyword_prompt)
        keywords = response.text.strip()
        print(self.get_recommendations(keywords))

# Create an instance of the ChatBot and get prompt from the user
ob = ChatBot()
ob.get_prompt()
