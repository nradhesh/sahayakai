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
        self.embedding = None
        with open("Vector.pkl", "rb") as f:
            self.embedding = pickle.load(f)
            print("Loaded.")
        genai.configure(api_key="AIzaSyAHZtgC-fHXDveWo0rzAEm4HaMGNAGVyVQ")
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    


    def get_recommendations(self,promt):
        vectorizer = TfidfVectorizer(stop_words='english')
        vec = vectorizer.fit_transform(promt)
        nfeatures = len(self.embedding.A[0])
        user_vec = np.pad(vec.A,((0,0),(0,nfeatures-len(vec.A[0]))))
        cosine_sim = cosine_similarity(self.embedding, user_vec).flatten()
        top_indices = cosine_sim.argsort()[-5:][::-1]
        top_schemes = [self.df.iloc[i][0] for i in top_indices]

        return top_schemes

    def getPromt(self):
        promt = input("Enter promt .")
        keyword_prompt = f"Extract only keywords from this for making cosine similarity with our database: {promt}. Give only keywords separated by space. Don't explain, don't put hyphen."
        response = self.model.generate_content(keyword_prompt)
        keywords = response.text.strip()
        print(self.get_recommendations([promt]))

ob = ChatBot()
ob.getPromt()
