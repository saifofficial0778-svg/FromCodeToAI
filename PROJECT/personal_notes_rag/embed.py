import os
import json
import uuid
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ============================================================
# SETTINGS
# ============================================================
COLLECTION_NAME = "personal_notes"

# True  = naye notes (agar hain) upload karo, phir sawaal pucho
# False = upload check bhi skip karo, seedha sawaal pucho
UPLOAD = True

# True  = sab kuch delete karke shuru se banao (model badla ya purani file update ki toh)
# False = purana data rakho, sirf NAYI files add karo
REBUILD = False

# yaha likha rehta hai ki kaunsi chunk files Qdrant me pehle se upload ho chuki hain
DONE_FILE = Path("data/uploaded_files.json")

# ============================================================
# PART 1 — CONNECT
# ============================================================
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
groq = Groq(api_key=GROQ_API_KEY)

# ============================================================
# PART 2 — LOAD EMBEDDING MODEL
# ============================================================
print("Loading embedding model...")
model = SentenceTransformer("BAAI/bge-m3")
EMBEDDING_SIZE = model.get_sentence_embedding_dimension()   # model se apne aap aayega

# ============================================================
# PART 3 — UPLOAD ONLY NEW NOTES TO QDRANT
# ============================================================
if UPLOAD:

    # --- collection ready karo ---
    exists = qdrant.collection_exists(collection_name=COLLECTION_NAME)

    # REBUILD ho, ya collection hai par tracking file nahi (pehli baar) -> shuru se banao
    if exists and (REBUILD or not DONE_FILE.exists()):
        print(f"Collection '{COLLECTION_NAME}' delete ho rahi hai (fresh start)...")
        qdrant.delete_collection(collection_name=COLLECTION_NAME)
        DONE_FILE.unlink(missing_ok=True)
        exists = False

    if not exists:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE)
        )
        print(f"Collection '{COLLECTION_NAME}' created.")

    # --- kaunsi files pehle upload ho chuki hain ---
    if DONE_FILE.exists():
        done = json.loads(DONE_FILE.read_text(encoding="utf-8"))
    else:
        done = []

    new_files = [
        file for file in sorted(Path("data/chunks").glob("*.jsonl"))
        if file.name not in done
    ]

    if not new_files:
        print("Koi nayi file nahi mili. Upload skip.")

    # --- sirf nayi files embed karke upload karo ---
    for file in new_files:

        documents = []

        for line in file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                documents.append(json.loads(line))

        print(f"{file.name}: {len(documents)} chunks embed ho rahe hain...")

        embeddings = model.encode(
            [doc["embed_text"] for doc in documents],
            normalize_embeddings=True
        )

        points = []

        for i, vector in enumerate(embeddings):

            point = PointStruct(
                # chunk id se fixed UUID banti hai, isliye purane points se kabhi nahi takrayegi
                id=str(uuid.uuid5(uuid.NAMESPACE_URL, documents[i]["id"])),
                vector=vector.tolist(),
                payload={
                    "text": documents[i]["text"],
                    "topic": documents[i]["topic"],
                    "section": documents[i]["section"],
                    "source": documents[i]["source"]
                }
            )

            points.append(point)

        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

        # yaad rakho ki ye file upload ho gayi
        done.append(file.name)
        DONE_FILE.parent.mkdir(parents=True, exist_ok=True)
        DONE_FILE.write_text(json.dumps(done, indent=2), encoding="utf-8")

        print(f"Uploaded {len(points)} chunks.")

# ============================================================
# PART 4 — SEARCH
# ============================================================
def search(query, top_k=3):

    query_vector = model.encode(query, normalize_embeddings=True).tolist()

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    ).points

    return results

# ============================================================
# PART 5 — ASK THE LLM
# ============================================================
def ask_llm(question, context):

    prompt = f"""
    Answer the question using only the notes given below.
    Answer in simple Hinglish.

    Notes:
    {context}

    Question:
    {question}

    If the answer is not present in the notes, say:
    "Mere notes me ye nahi mila . Thank You !"
    """

    response = groq.chat.completions.create(
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
# PART 6 — ASK QUESTIONS (loop)
# ============================================================
print("\nApne notes se kuch bhi pucho. Band karne ke liye 'exit' likho.")

while True:

    question = input("\nQuestion: ").strip()

    if question.lower() in ("exit", "quit"):
        break

    if not question:
        continue

    results = search(question, top_k=3)

    print("\nMile hue chunks:")
    for result in results:
        print(f"  Score: {result.score:.3f}  |  {result.payload['topic']} > {result.payload['section']}")

    context = "\n\n---\n\n".join(
        result.payload["text"]
        for result in results
    )

    answer = ask_llm(question, context)

    print("\nAnswer:")
    print(answer)