import os
import numpy as np
from sentence_transformers import SentenceTransformer

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

model=SentenceTransformer('all-MiniLM-L6-v2')#384

# text="Machine learning is fun"
# res=model.encode(text)
# embedding=model.encode(text)
# print(embedding[:10])

t1="cats are domestic animals"
t2="domestic animals are those animals that are tamed and kept by humans"

v1=model.encode(t1)
v2=model.encode(t2)

similarity=cosine_similarity(v1, v2)
print(similarity)
