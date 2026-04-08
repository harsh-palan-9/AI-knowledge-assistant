from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

INDEX_NAME = os.getenv("PINECONE_INDEX")

# Create index if not exists
if INDEX_NAME not in [i.name for i in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,  # MUST match embedding size
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",        # or "gcp"
            region="us-east-1"  # safe default
        )
    )

# Connect to index
index = pc.Index(INDEX_NAME)

print(pc.list_indexes())