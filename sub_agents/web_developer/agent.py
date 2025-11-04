from langchain.agents import create_agent
from agent.model import model
from sub_agents.web_developer.tools import create_html_file, create_css_file, create_js_file, append_to_file
from sub_agents.web_developer.system_prompt import get_system_prompt

tools = [
    create_html_file,
    create_css_file,
    create_js_file,
    append_to_file,
]

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=get_system_prompt(),
)

def ask_web_developer_agent(user_text: str):
    """Invoke the web developer agent with a single user message, return the final assistant text."""
    agent.system_prompt = get_system_prompt()
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_text}]},
    )
    try:
        last_msg = result["messages"][-1].content
    except Exception:
        last_msg = str(result)
    return last_msg