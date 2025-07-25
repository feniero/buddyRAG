from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

#variables
embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
llm_model = os.getenv("LLM_MODEL", "llama3.1:8b")
print("embeddings_model: ",embedding_model)
print("llm_model: ",llm_model)


app = FastAPI()
class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_q(q: Question):
    # 1. embedding the question
    try:
        embed_resp = requests.post(
            "http://ollama:11434/api/embeddings",
            json={
                "model": embedding_model,
                "prompt": q.query
            }
        )
        embed_resp.raise_for_status()
        embedding = embed_resp.json()["embedding"]

        print("question embedded:",embedding)

    except Exception as e:
        return {"error": f"Failed to retrieve embeddings from Ollama: {e}"}

    # 2. search on weaviate
    try:
        graphql_query = {
            "query": """
            {
              Get {
                Document(
                  nearVector: {
                    vector: %s
                  },
                  limit: 3
                ) {
                  content
                }
              }
            }
            """ % str(embedding).replace("'", "")
        }

        weaviate_resp = requests.post(
            "http://weaviate:8080/v1/graphql",
            json=graphql_query
        )
        weaviate_resp.raise_for_status()
        docs = "\n".join([d['content'] for d in weaviate_resp.json()['data']['Get']['Document']])

        print("Docs used for prompt:\n", docs)

    except Exception as e:
        return {"error": f"Failed to retrieve docs from weaviate: {e}"}

    # 3. generate Ollama respose
    try:
        ollama_resp = requests.post(
            "http://ollama:11434/api/generate",
            json={
                "model": llm_model,
                "prompt": f"Reply with this context:\n{docs}\nQuestion: {q.query}",
                "stream": False,
            }
        )
        ollama_resp.raise_for_status()
        answer = ollama_resp.json()["response"]

        print("Ollama respose:", answer)

    except Exception as e:
        return {"error": f"Failed to generate Ollama respose: {e}"}

    return {"answer": answer}
