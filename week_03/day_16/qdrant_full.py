# ============================================================
# PART 1 — IMPORTS AND ENVIRONMENT
# ============================================================

import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue, MatchAny, PayloadSchemaType
from sentence_transformers import SentenceTransformer
from groq import Groq
import json

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")    

# ============================================================
# PART 2 — CONNECT TO QDRANT
# ============================================================
client={
    "qdrant": QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY),
    "groq": Groq(api_key=GROQ_API_KEY)
}

# ============================================================
# PART 3 — CREATE QDRANT COLLECTION
# ============================================================
COLLECTION_NAME = "Knowledge_filter"
EMBEDDING_SIZE = 384

#Delete collection if it exists
if client["qdrant"].collection_exists(collection_name=COLLECTION_NAME):
    print(f"Collection '{COLLECTION_NAME}' already exists. Deleting it...")
    client["qdrant"].delete_collection(collection_name=COLLECTION_NAME)
    
#Create collection
client["qdrant"].create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE)
)

print(f"Collection '{COLLECTION_NAME}' created successfully.")
print(f"vector size: {EMBEDDING_SIZE}")
print(f"distance metric: {Distance.COSINE}")
client["qdrant"].create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD,
)

with open("knowledge.json", "r", encoding="utf-8") as f:
    documents = json.load(f)
    
# ============================================================
# PART 5 — CREATE EMBEDDINGS
# ============================================================
    

print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions

print("Embedding model ready!")
texts = [document["text"] for document in documents]

embeddings = model.encode(texts)

print(f"Generated {len(embeddings)} embeddings")
print(f"Embedding size: {len(embeddings[0])}")

# ============================================================
# PART 6 — CREATE QDRANT POINTS
# ============================================================

points=[]

for i in range(len(documents)):
    
    point = PointStruct(
        id=i + 1,
        vector=embeddings[i].tolist(),
        payload=documents[i]
    )

    points.append(point)
    
# ============================================================
# PART 7 — UPLOAD TO QDRANT
# ============================================================

client["qdrant"].upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print(f"Uploaded {len(points)} documets to Qdrant")

# ============================================================
# PART 8 — SEARCH QDRANT
# ============================================================

def search(query,top_k=3):
    
    query_vector=model.encode(query).tolist()
    
    results=client["qdrant"].query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    ).points
    
    return results

def search_with_filter(query, query_filter=None, top_k=3):


    query_vector = model.encode(query).tolist()


    results = client["qdrant"].query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
        query_filter=query_filter,
    ).points


    return results

reimbursement_filter = Filter(
    must=[
        FieldCondition(
            key="category",
            match=MatchValue(value="reimbursement")
        )
    ]
)

# ============================================================
# PART 9 — TEST SEARCH
# ============================================================

query="How many vaccation days do i get"

results=search_with_filter(query,reimbursement_filter,top_k=3)

print("\nSearch results :")

for result in results:
    print(f"Score:{result.score:.3f}")
    print(result.payload["text"])
    print()
    
# ============================================================
# PART 11 — ASK THE LLM
# ============================================================

def ask_llm(question, context):

    prompt = f"""
    Answer the question using only the information provided below.

    Context:
    {context}

    Question:
    {question}

    If the answer is not present in the context, say:
    "I don't know based on the provided information."
    """

    response = client["groq"].chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
    
# ============================================================
# PART 12 — COMPLETE RAG PIPELINE
# ============================================================

question = "kya meko koi other laabh mil rha hai salary ke alawa ans in eng?"

results = search_with_filter(question,reimbursement_filter, top_k=3)


# Extract text from the search results
context = "\n".join(
    result.payload["text"]
    for result in results
)


answer = ask_llm(question, context)


print("\nFinal Answer:")
print(answer)