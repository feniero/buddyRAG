#!/bin/bash

echo "Starting Ollama server..."
ollama serve &

echo "Waiting for Ollama server to be active..."
while [ "$(ollama list | grep 'NAME')" == "" ]; do
  sleep 1
done

# Pull embedding model
if [ -n "$EMBEDDING_MODEL" ]; then
  echo "Pulling embedding model: $EMBEDDING_MODEL"
  ollama pull "$EMBEDDING_MODEL"
fi

# Pull LLM model
if [ -n "$LLM_MODEL" ]; then
  echo "Pulling LLM model: $LLM_MODEL"
  ollama pull "$LLM_MODEL"
fi

echo "All models have been pulled..."
touch /tmp/ollama_ready.flag

wait $!
