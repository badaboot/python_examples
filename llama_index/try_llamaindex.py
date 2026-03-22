from llama_index.llms.ollama import Ollama
# this is somehow very slow. why not use ollama directly? 
llm = Ollama(
    model="llama3.1",
    request_timeout=120.0,
    # Manually set the context window to limit memory usage
    context_window=8000,
)
resp = llm.complete("Who is Paul Graham?")
print(resp)
