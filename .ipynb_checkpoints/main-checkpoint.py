import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("VectoredSchemes.csv")

def startUp():
    schemes = np.array()
    for i in df