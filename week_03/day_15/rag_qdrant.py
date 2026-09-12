import os
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")    

#part2: CONNECT TO QDRANT
client={
    "qdrant": QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY),
    "groq": Groq(api_key=GROQ_API_KEY)
}

#part3: CREATE COLLECTION
COLLECTION_NAME = "Knowledge"
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

with open("knowledge.txt", "r", encoding="utf-8") as f:
    documents = [
        line.strip() 
        for line in f.readlines()
        if line.strip()
        ]
    
print (f"Loaded {len(documents)} documents from 'knowledge.txt'.")

#part5: EMBEDDING AND UPLOAD TO QDRANT
print("Embedding and uploading documents to Qdrant...")
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions

embeddings = model.encode(documents)
print(f"Generated embeddings for {len(embeddings)} documents.")
print(f"Embedding size: {len(embeddings[0])}")

#part 6 create qdrant points

points=[]

for i , doc in enumerate(embeddings):
    
    point=PointStruct(
        id =i+1,
        vector=doc.tolist(),
        payload={
            "text":documents[i]
        }
        
    )
    
    points.append(point)
    
# part 7 upload to qdrant

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

# ============================================================
# PART 9 — TEST SEARCH
# ============================================================

query="How many vaccation days do i get"

results=search(query,top_k=3)

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

question = "hlo how are you"

results = search(question, top_k=3)


# Extract text from the search results
context = "\n".join(
    result.payload["text"]
    for result in results
)


answer = ask_llm(question, context)


print("\nFinal Answer:")
print(answer)