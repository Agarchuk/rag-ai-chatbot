#!/bin/bash

/bin/ollama serve &
pid=$!

while ! curl -s http://localhost:11434 > /dev/null; do
    echo "⏳ Waiting for the Ollama server to start..."
    sleep 2
done
echo "🟢 Ollama server is up and running!"


echo "🔴 Starting the process of downloading the LLAMA3 model..."
echo "🔄 Please wait while we retrieve the model..."
ollama pull smollm2:135m

if [ $? -eq 0 ]; then
    echo "🟢 LLAMA3 model downloaded successfully!"
else
    echo "🔴 Failed to download the LLAMA3 model."
fi

wait $pid
