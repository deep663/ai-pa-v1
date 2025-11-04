# agent/agent.py
from langchain.agents import create_agent
from agent.model import model


# import tools
from tools.excel_tools import create_excel, add_row, read_excel, update_cell, delete_row
from tools.project_tools import create_project, list_projects, update_project_status, delete_project
from tools.system_tools import  make_backup, check_internet
from tools.reminders_tools import add_reminder, get_reminder, delete_reminder, list_reminders
from tools.file_tools import read_any_file, list_files, find_files, write_file
from tools.web_tools import advanced_web_search, find_jobs, search_youtube_video, open_youtube_video, play_youtube_video
from tools.fs_tools import create_directory, delete_directory, move_directory, find_files_by_name, read_directory
from tools.sys_tools import run_shell_command, get_system_info, open_application
from tools.document_tools import attach_document, list_documents, read_document, delete_document
from tools.sub_agent_tools import delegate_to_web_developer

from agent.memory import  *
from agent.context import *
from agent.system_prompt import get_system_prompt

state = CustomAgentState(
    user_id="1",
    usr_pref = {},
)

tools = [
    create_excel, add_row, read_excel, update_cell, delete_row,
    create_project, list_projects, update_project_status, delete_project,
    check_internet, make_backup,
    add_reminder, get_reminder, delete_reminder, list_reminders,
    read_any_file, list_files, find_files, write_file,
    advanced_web_search,
    find_jobs,
    search_youtube_video,
    open_youtube_video,
    play_youtube_video,
    create_directory, delete_directory, move_directory, find_files_by_name, read_directory,
    run_shell_command, get_system_info, open_application,
    attach_document,
    list_documents,
    read_document,
    delete_document,
    delegate_to_web_developer
]

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=get_system_prompt(),
    checkpointer=sqliteSaver,
    store=sqliteStore,
    middleware=[semantic_context_recall]
)

def ask_agent(user_text: str):
    """Invoke the agent with a single user message, return the final assistant text."""
    # Update the system prompt with the current time before each invocation
    agent.system_prompt = get_system_prompt()
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
