from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.sqlite import SqliteStore
from langchain_ollama.embeddings import OllamaEmbeddings
import sqlite3

conn1 = sqlite3.connect("memory.db", check_same_thread=False)
sqliteSaver = SqliteSaver(conn1)


conn2 = sqlite3.connect("longterm_memory.db", check_same_thread=False, isolation_level=None)
sqliteStore = SqliteStore(
    conn2,
    index={
        "dims": 768,
        "embed": OllamaEmbeddings(model="mxbai-embed-large"),  
        "fields": ["text"]
    },
)

conn3 = sqlite3.connect("agent_memory.db", check_same_thread=False, isolation_level=None)
AgentStore = SqliteStore(
    conn3,
    index={
        "dims": 768,
        "embed": OllamaEmbeddings(model="mxbai-embed-large"),  
        "fields": ["text"]
    },
)

# sqliteSaver.setup()
# sqliteStore.setup()
# AgentStore.setup() 