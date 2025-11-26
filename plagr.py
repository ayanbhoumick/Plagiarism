import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# loading all (.txt) files in current directory
student_files = [doc for doc in os.listdir() if doc.endswith('.txt')]
student_notes = [open(_file, encoding='utf-8').read() for _file in student_files]

def vectorize(text):
    return TfidfVectorizer().fit_transform(text).toarray()

def similarity(doc1, doc2):
    return cosine_similarity([doc1], [doc2])[0][0]

vectors = vectorize(student_notes)
s_vectors = list(zip(student_files, vectors))
plagiarism_results = set()

def check_plagiarism():
    global s_vectors
    for student_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]

        for student_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)
            plagiarism_results.add((student_a, student_b, sim_score))

check_plagiarism()

#for clean output
for a, b, score in plagiarism_results:
    percent = score * 100
    print(f"{a} ↔ {b} : {percent:.2f}% similar")