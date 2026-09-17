from langchain_text_splitters import (CharacterTextSplitter,RecursiveCharacterTextSplitter)

text=""""Artificial Intelligence is changing the way software applications are built. It allows computers to perform tasks that normally require human intelligence, such as understanding text, recognizing patterns, and making predictions.

Generative AI is a branch of artificial intelligence that can create new content. It can generate text, images, code, audio, and other types of content based on the input given by the user.

Retrieval Augmented Generation, commonly called RAG, combines information retrieval with a Large Language Model. Instead of relying only on the model's internal knowledge, RAG retrieves relevant information from external data and provides it to the model as context.

Vector databases are commonly used in RAG systems to store and search embeddings. An embedding represents text as a numerical vector, allowing the system to find documents that are semantically similar to a user's query.

Chunking is an important step in a RAG pipeline. Large documents are divided into smaller pieces called chunks before creating embeddings. Good chunking helps the retrieval system find relevant information more accurately."""

#================================================================
# 1. Fixed size Chunking
#================================================================

fixed=CharacterTextSplitter(
    separator="",
    chunk_size=100,
    chunk_overlap=0
)
# chunks = fixed.split_text(text)
# print('\n=========Fixed Size=========')

# for chunk in chunks:
#     print(chunk)
#     print('------------')
    
    
#================================================================
# 1. Paragraph Chunking
#================================================================
paragraph=CharacterTextSplitter(
    separator="\n\n",
    chunk_size=300,
    chunk_overlap=0
)

# chunks = paragraph.split_text(text)
# print('\n=========Paragraph Size=========')

# for chunk in chunks:
#     print(chunk)
#     print('------------')
    
#================================================================
# 1. Recursive Chunking
#================================================================

recursive = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

chunks = recursive.split_text(text)
print('\n=========Recursive Size=========')

for chunk in chunks:
    print(chunk)
    print('------------')