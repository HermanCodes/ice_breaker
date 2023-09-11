from langchain import PromptTemplate
from langchain.chat_models import AzureChatOpenAI

from langchain.agents import initialize_agent, Tool, AgentType

from tools.tools import get_profile_url


def lookup(name: str) -> str:
    llm = AzureChatOpenAI(deployment_name="RegMarketGpt35Turbo", temperature=0)
    template = """Given the full name {name_of_person}, I want you to get me a link to their LinkedIn profile page. 
    Your answer should contain only a URL.
    """

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url,
            description="this tool is useful for when you need to find a LinkedIn profile page for a person",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        llm=llm,
        verbose=True,
    )
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    linkedin_profile_url = agent.run(prompt_template.format_prompt(name_of_person=name))
    return linkedin_profile_url
