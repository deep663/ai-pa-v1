from langchain.tools import tool
from sub_agents.web_developer.agent import ask_web_developer_agent

@tool
def delegate_to_web_developer(request: str) -> str:
    """Delegate a web development task to the web developer sub-agent.

    Args:
        request (str): The user's request for the web developer sub-agent.

    Returns:
        str: The response from the web developer sub-agent.
    """
    return ask_web_developer_agent(request)