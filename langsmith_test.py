from langchain_ollama import OllamaLLM
import sys

# Check if arguments were passed
if len(sys.argv) > 1:
    print(f"First argument: {sys.argv[1]}")
else:
    print("No arguments provided.")
    sys.exit(1)

# # Initialize the local Ollama model
model = OllamaLLM(model="llama3.2", keep_alive="2h")

# Invoke the model; LangSmith will automatically capture the trace
response = model.invoke(sys.argv[1])
print(response)
