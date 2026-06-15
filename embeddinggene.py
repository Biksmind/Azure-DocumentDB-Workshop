from pymongo import MongoClient
from openai import AzureOpenAI
import os

# -----------------------------
# Azure OpenAI Configuration
# -----------------------------
AZURE_OPENAI_ENDPOINT = "https://<your-openai-resource>.openai.azure.com/"
AZURE_OPENAI_KEY = "<your-azure-openai-key>"
AZURE_OPENAI_API_VERSION = "2024-02-01"
EMBEDDING_DEPLOYMENT = "text-embedding-3-small"  
# example: text-embedding-3-small

# -----------------------------
# Azure DocumentDB Connection
# -----------------------------
MONGO_URI = "<your-documentdb-connection-string>"

DB_NAME = "Workshop_DB"
COLLECTION_NAME = "supportInc"

# -----------------------------
# Clients
# -----------------------------
openai_client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version=AZURE_OPENAI_API_VERSION
)

mongo_client = MongoClient(MONGO_URI)
collection = mongo_client[DB_NAME][COLLECTION_NAME]


def generate_embedding(text: str):
    response = openai_client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT,
        input=text
    )
    return response.data[0].embedding


# -----------------------------
# Generate and update embeddings
# -----------------------------
tickets = collection.find({})

for ticket in tickets:
    text_for_embedding = f"""
    Title: {ticket.get('title', '')}
    Description: {ticket.get('description', '')}
    Category: {ticket.get('category', '')}
    Priority: {ticket.get('priority', '')}
    """

    embedding = generate_embedding(text_for_embedding)

    collection.update_one(
        {"_id": ticket["_id"]},
        {
            "$set": {
                "embedding": embedding,
                "embeddingText": text_for_embedding.strip()
            }
        }
    )

    print(f"Updated embedding for {ticket['ticketId']}")

print("All embeddings generated successfully.")