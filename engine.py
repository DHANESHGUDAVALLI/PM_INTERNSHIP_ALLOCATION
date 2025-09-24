import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
students = pd.read_csv("data/students.csv")
internships = pd.read_csv("data/internships.csv")

# TF-IDF for skill matching
vectorizer = TfidfVectorizer()

# Convert internship skills into vector space
internship_vectors = vectorizer.fit_transform(internships["required_skills"])

def recommend_internship(student_id):
    student = students[students["student_id"] == student_id].iloc[0]
    student_vector = vectorizer.transform([student["skills"]])

    # Calculate similarity
    similarity_scores = cosine_similarity(student_vector, internship_vectors).flatten()

    # Find best match
    best_index = similarity_scores.argmax()
    best_internship = internships.iloc[best_index]

    return {
        "student_name": student["name"],
        "skills": student["skills"],
        "best_match": best_internship["company_name"],
        "required_skills": best_internship["required_skills"],
        "location": best_internship["location"],
        "sector": best_internship["sector"]
    }

# Test with one student
if __name__ == "__main__":
    result = recommend_internship(1)
    print(result)
