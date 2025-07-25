import os
import time
import requests

INPUT_DIR = "./input_files"
embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

def embed_text(text):
    print("embedding the docs")
    resp = requests.post("http://ollama:11434/api/embeddings", json={
        "model": embedding_model,
        "prompt": text
    })
    return resp.json()["embedding"]

def send_to_weaviate(content, vector):
    print("Sending content to weaviate")
    return requests.post("http://weaviate:8080/v1/objects", json={
        "class": "Document",
        "properties": {
            "content": content,
        },
        "vector": vector
    })

def process_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()
        vec = embed_text(content)
        send_to_weaviate(content, vec)
    # renaming vectorized docs
    dirname, fname = os.path.split(filepath)
    os.rename(filepath, os.path.join(dirname, "_" + fname))

def main():
    print(f"Watching directory: {INPUT_DIR}")
    os.makedirs(INPUT_DIR, exist_ok=True)
    while True:
        for fname in os.listdir(INPUT_DIR):
            if not fname.endswith(".md") or fname.startswith("_"):
                continue
            full_path = os.path.join(INPUT_DIR, fname)
            try:
                process_file(full_path)
                print(f"process file: {fname}")
            except Exception as e:
                print(f"Failed to process file {fname}: {e}")
        time.sleep(2)

if __name__ == "__main__":
    main()
