from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
import asyncio
import os
import time
from llama_index.core import PromptTemplate

class TimedOllama(Ollama):
    async def acomplete(self, prompt, **kwargs):
        t1 = time.time()
        result = await super().acomplete(prompt, **kwargs)
        t2 = time.time()
        print(f"LLM call took: {t2 - t1:.2f}s")
        return result

Settings.llm = TimedOllama(
    model="llama3.2:latest",
    system_prompt="You are a helpful, concise assistant. Only answers questions contained in the provided text. Answer 'I don't know' if the answer is not in the provided text.",
    request_timeout=180.0, # 3 minutes
    context_window=8000,
    # keep model alive for 24 hours to speed up subsequent calls (no need to reload the model)
    keep_alive="24h"
)
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    base_url="http://localhost:11434",
)

STORAGE_DIR = "storage"

if os.path.exists(STORAGE_DIR):
    print("Loading index from storage...")
    storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
    index = load_index_from_storage(storage_context)
else:
    print("Loading documents...")
    documents = SimpleDirectoryReader("literature").load_data()
    print(f"Loaded {len(documents)} documents")

    print("Building index (this embeds all chunks)...")
    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    print("Index built, persisting...")
    index.storage_context.persist(STORAGE_DIR)

query_engine = index.as_query_engine(
    response_mode="compact",
    similarity_top_k=4,
) 

async def main():
    print("Running query...")
    t1 = time.time()
    response = await query_engine.aquery("Who is the first person to land on the moon?") # what is this article about?
    t2 = time.time()
    print(f"Embed + search + llm took: {t2 - t1:.2f}s")  
    print(response)

if __name__ == "__main__":
    asyncio.run(main())