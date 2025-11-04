# agent/model.py
from dotenv import load_dotenv
import os
from rich.console import Console
from langchain.chat_models import init_chat_model

load_dotenv()
console = Console()

try:
    model = init_chat_model("ollama:gpt-oss:120b-cloud", temperature=0.2, timeout=30)
    console.print("[bold green]Using gpt-oss:120b-cloud model from Ollama.[/bold green]")
except Exception as e:
    console.print(f"[bold red]Could not initialize gpt-oss:120b-cloud, falling back to local LLM. Error: {e}[/bold red]")
    model = init_chat_model("ollama:qwen3:4b", temperature=0.2, timeout=30)

