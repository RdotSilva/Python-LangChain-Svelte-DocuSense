import os
import pinecone
from langchain.vectorstores.pinecone import Pinecone

pinecone.Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV_NAME"),
)
