#!/bin/bash

# Start Ollama
/bin/ollama serve &

# Track the PID of the last background process
pid=$!

# Fetch the LLAMA2 model
echo "Pulling LLAMA2 model..."
ollama pull llama2-uncensored:latest
echo "Model pulled successfully!"

# Sit idle until the background process is done (never unless it does)
wait $pid