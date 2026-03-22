from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import SimpleDirectoryReader
# this is fast because no chunking
ollama_embedding = OllamaEmbedding(
    model_name="nomic-embed-text",
    base_url="http://localhost:11434",
)

# Load documents from data folder
documents = SimpleDirectoryReader("literature").load_data()
passages = [doc.text for doc in documents]

embeddings = ollama_embedding.get_text_embedding_batch(
    passages, show_progress=True
)
print(f"Got vectors of length {len(embeddings[0])}")
print(embeddings[0][:10])