import os
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer

model=SentenceTransformer('all-MiniLM-L6-v2')#384

load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError(
        "GROQ_API_KEY environment variable is not set. Please set it in your .env file."
    )
    
client = Groq(api_key=my_api_key)
groq_model="openai/gpt-oss-120b"

documents = [
    "Employees receive 24 days of paid leave per year.",
   
    "Employees work from the office on Tuesday, Wednesday and Thursday. "
    "Monday and Friday are optional work-from-home days.",
   
    "Employees receive Rs 3000 per month for gym reimbursement.",
   
    "Employees can claim Rs 2000 per month for home internet.",
   
    "Employees have a 90 day notice period."
]

document_embeddings = model.encode(documents)
print()

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

SIMILARITY_THRESHOLD = 0.3
def retrieve(query_embedding):
    scores=[]
    for i,doc_embedding in enumerate(document_embeddings):
        score=cosine_similarity(query_embedding, doc_embedding)
        scores.append((score, documents[i]))               
    
    scores.sort(reverse=True)
     
    best_score, best_document = scores[0]
    
    print(f"Similarity Score: {best_score:.3f}")
   
    if best_score < SIMILARITY_THRESHOLD:
        return None, None
    return best_score, best_document


def ask_llm(question,context):

    sys_prompt=f"""answer in one line only. Answer only based on this context. do not hallucinate. Context: {context}"""
    system_message={
        "role": "system",
        "content": sys_prompt

    }
    message={
        "role": "user",
        "content": question
    }
    messages=[system_message, message]
    response=client.chat.completions.create(model=groq_model, messages=messages)
    answer=response.choices[0].message.content
    return answer

query = "gym ke pese mil rhe hai kya? ans in english"
query_embedding = model.encode(query)

score,context=retrieve(query_embedding)
if context is None:
    print("Sorry, I don't have information about this.")
else:
    answer = ask_llm(query, context)
    print(answer)
