from typing import Any, Dict
from langchain_ollama.chat_models import ChatOllama
from langchain.agents.middleware import before_model, after_model
from langgraph.runtime import Runtime
from langchain.agents import AgentState
from agent.memory import sqliteStore
import traceback
import time

MAX_RUNTIME_MESSAGES = 5
MAX_STORED_BATCH = 10

class CustomAgentState(AgentState):
    user_id: str
    usr_pref: Dict[str, Any] | None = None

@before_model
def smart_context_trimmer(state: "CustomAgentState", runtime: Runtime):
    messages = state.get("messages", [])
    user_id = state.get("user_id", "unknown")

    if len(messages) > MAX_RUNTIME_MESSAGES:
        old_msgs = messages[:-MAX_STORED_BATCH]
        state["messages"] = messages[-MAX_STORED_BATCH:]

        try:
            print("[Memory Archive]: Trimming memory archive...")
            text_dump = "\n".join([m.content for m in old_msgs])
            # Store for retrieval AND semantic search
            sqliteStore.put(
                ("memory_archive", user_id),
                f"chat_{int(time.time())}",
                {
                    "messages": [m.model_dump() for m in old_msgs],
                    "text": text_dump
                },
            )

        except Exception as e:
            print(f"[Memory Archive Error]: {e}")
            traceback.print_exc()



    return state


@after_model
def semantic_context_recall(state, runtime):
    """
    If assistant or user mentions something that seems out of current context,
    automatically retrieve semantically similar past messages.
    """
    user_id = state.get("user_id", "unknown")
    messages = state.get("messages", [])
    if not messages:
        return state

    last_msg = messages[-1].content.lower()

    # Trigger on curiosity or continuation words
    recall_triggers = ["remember", "earlier", "last time", "previous", "project", "before", "again"]

    if any(word in last_msg for word in recall_triggers):
        try:
            results = sqliteStore.search(
                ("memory_archive", user_id),
                query=last_msg,
                limit=2
            )
            if results:
                recalled_segments = []
                for _, _, archive in results:
                    if archive and "messages" in archive:
                        recalled_segments.extend(archive["messages"])

                if recalled_segments:
                    print(f"[Semantic Recall]: Retrieved {len(recalled_segments)} messages by meaning.")
                    state["messages"] = recalled_segments[-10:] + state["messages"]

        except Exception as e:
            print(f"[Semantic Recall Error]: {e}")
            traceback.print_exc()

    return state