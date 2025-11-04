from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.sqlite import SqliteStore
from langchain_ollama.embeddings import OllamaEmbeddings
import sqlite3

# Use in-memory saving for faster checkpoints
conn2 = sqlite3.connect("memory.db", check_same_thread=False,  isolation_level=None)
sqliteSaver = SqliteSaver(conn2)


conn3 = sqlite3.connect("memory_store.db", check_same_thread=False,  isolation_level=None)
sqliteStore = SqliteStore(
    conn3,
    index={
        "dims": 768,
        "embed": OllamaEmbeddings(model="mxbai-embed-large"),  
        "fields": ["text"]
    },
)

sqliteStore.setup()