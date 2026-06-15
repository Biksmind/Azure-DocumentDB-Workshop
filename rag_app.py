from pymongo import MongoClient
from openai import AzureOpenAI

# -----------------------------
# Azure OpenAI Configuration
# -----------------------------
AZURE_OPENAI_ENDPOINT = "https://<your-openai-resource>.openai.azure.com/"
AZURE_OPENAI_KEY = "<your-azure-openai-key>"
AZURE_OPENAI_API_VERSION = "2024-02-01"

EMBEDDING_DEPLOYMENT = "text-embedding-3-small"
CHAT_DEPLOYMENT = "gpt-4.1-mini"
# Example: gpt-4o-mini or gpt-4o

# -----------------------------
# Azure DocumentDB Configuration
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


def vector_search(user_question: str, top_k: int = 2):
    query_vector = generate_embedding(user_question)

    pipeline = [
        {
            "$search": {
                "cosmosSearch": {
                    "vector": query_vector,
                    "path": "embedding",
                    "k": top_k
                },
                "returnStoredSource": True
            }
        },
        {
            "$project": {
                "_id": 0,
                "ticketId": 1,
                "title": 1,
                "description": 1,
                "category": 1,
                "priority": 1,
                "score": {"$meta": "searchScore"}
            }
        }
    ]

    return list(collection.aggregate(pipeline))


def build_context(search_results):
    context = ""

    for item in search_results:
        context += f"""
Ticket ID: {item.get("ticketId")}
Title: {item.get("title")}
Description: {item.get("description")}
Category: {item.get("category")}
Priority: {item.get("priority")}
Score: {item.get("score")}
---
"""

    return context.strip()


def generate_answer(user_question: str, context: str):
    system_prompt = """
You are a support assistant.
Answer the user's question using only the provided support ticket context.
If the answer is not present in the context, say that you do not have enough information.
Keep the answer simple and clear.
"""

    user_prompt = f"""
User Question:
{user_question}

Support Ticket Context:
{context}

Answer:
"""

    response = openai_client.chat.completions.create(
        model=CHAT_DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


def main():
    print("\nAzure DocumentDB RAG Demo")
    print("Type 'exit' to stop.\n")

    while True:
        user_question = input("Ask your question: ")

        if user_question.lower() == "exit":
            break

        print("\nSearching Azure DocumentDB...\n")

        results = vector_search(user_question)

        print("Retrieved Tickets:")
        for item in results:
            print(f"- {item['ticketId']} | {item['title']} | Score: {item.get('score')}")

        context = build_context(results)

        print("\nGenerating answer using Azure OpenAI...\n")

        answer = generate_answer(user_question, context)

        print("\nAnswer:")
        print(answer)
        print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    main()