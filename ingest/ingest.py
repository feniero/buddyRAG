import os
import requests
import json

INPUT_DIR = "./input_files"

embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

def embed_text(text):
    resp = requests.post("http://ollama:11434/api/embeddings", json={
        "model": embedding_model,
        "prompt": text
    })
    return resp.json()["embedding"]

def send_to_weaviate(content, vector):
    return requests.post("http://weaviate:8080/v1/objects", json={
        "class": "Document",
        "properties": {
            "content": content,
        },
        "vector": vector
    })

def main():
    for fname in os.listdir(INPUT_DIR):
        if not fname.endswith(".md") or fname.startswith("_"):
            continue
        with open(os.path.join(INPUT_DIR, fname)) as f:
            content = f.read()
            vec = embed_text(content)
            send_to_weaviate(content, vec)
            os.rename(
                os.path.join(INPUT_DIR, fname),
                os.path.join(INPUT_DIR, "_" + fname)
            )

if __name__ == "__main__":
    main()
