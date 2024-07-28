import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyAHZtgC-fHXDveWo0rzAEm4HaMGNAGVyVQ")

model = genai.GenerativeModel('gemini-1.5-flash')

query = input("Enter your promt: ")
response = model.generate_content(f"Extract only keywords from this for making cosine similarity with our database: {query} Give only keywords separated by space. Dont explain, dont put hyphen.")
print([response.text])
