from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# 1. Define your tool with the @tool decorator
@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# 2. Use ChatOllama instead of claude-sonnet
llm = ChatOllama(
    model="llama3.2:latest",   # or mistral, qwen2.5, etc. — must support tool calling
    base_url="http://localhost:11434",  # default Ollama URL
)

# 3. Build a prompt with required placeholders
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),  # required for tool call history
])

# 4. Wire everything together
agent = create_tool_calling_agent(llm, [get_weather], prompt)
agent_executor = AgentExecutor(agent=agent, tools=[get_weather], verbose=True)

# 5. Run it
result = agent_executor.invoke({"input": "what is history of henderson, Nevada?"})
print(result["output"])