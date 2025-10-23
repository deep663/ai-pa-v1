# agent/model.py
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:3b")

# model = ChatOllama(model=MODEL_NAME, temperature=0.1, timeout=30)

model = init_chat_model("ollama:llama3.2:3b", temperature=0.1, timeout=30)
