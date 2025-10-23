# agent/agent.py
from langchain.agents import create_agent
from agent.model import model
from pathlib import Path
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore


# import tools
from tools.excel_tools import create_excel, add_row, read_excel, update_cell, delete_row
from tools.project_tools import create_project, list_projects, update_project_status, delete_project
from tools.system_tools import  make_backup, check_internet, get_current_time, get_today
from tools.reminders_tools import add_reminder, get_reminder, delete_reminder
from tools.file_tools import read_any_file, list_files
from tools.pdf_tools import read_pdf_file
from tools.web_tools import advanced_web_search

from agent.memory import  *
from agent.context import *
from agent.system_prompt import SYS_PROMPT

state = CustomAgentState(
    user_id="1",
    usr_pref = {},
)

tools = [
    create_excel, add_row, read_excel, update_cell, delete_row,
    create_project, list_projects, update_project_status, delete_project,
    check_internet, make_backup, get_today, get_current_time,
    add_reminder, get_reminder, delete_reminder,
    read_any_file, list_files,
    read_pdf_file,
    advanced_web_search
]

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYS_PROMPT,
    checkpointer=sqliteSaver,
    store=sqliteStore,
    context_schema=CustomAgentState,
    middleware=[smart_context_trimmer, semantic_context_recall]
)

def ask_agent(user_text: str):
    """Invoke the agent with a single user message, return the final assistant text."""
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_text}]},
        {"configurable": {"thread_id": "user_admin"}},
        context={"user_id":"001"},
        )
    # result is a dict-like object. The last message is the latest assistant message.
    try:
        last_msg = result["messages"][-1].content
        # print('[debug]: ',result)
    except Exception:
        # fallback: convert to string
        last_msg = str(result)
    return last_msg
