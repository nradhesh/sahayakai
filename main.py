import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("VectoredSchemes.csv")
schemes = []
def startUp():
    schemes = np.array()
    for i in df:
        row = [int(i) for i in df.iloc[i][-4][1:-1].split(',')]
        col = [int(i) for i in df.iloc[i][-3][1:-1].split(',')]
        vec = [int(i) for i in df.iloc[i][-2][1:-1].split(',')]
        arr = np.zeros(row[0], col[0])
        for i in range(1,len(row)):
            arr[row[i]][col[i]] = vec[i]
        schemes.append(arr)

def get_recommendations(promt_vec):
    cosine_sim = cosine_similarity(schemes, promt_vec).flatten()
    top_indices = cosine_sim.argsort()[-5:][::-1]
    top_schemes = [df.iloc[i] for i in top_indices]

    return top_schemes
